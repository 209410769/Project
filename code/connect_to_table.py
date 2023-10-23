import psycopg2
import os
import glob
from datetime import datetime
import re

# 資料庫連線參數
db_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '0000',
    'port': '5432'
}

# 資料來源資料夾
source_folder = "/Users/jimmy/Desktop/Jimmy/Project/code/data/RVR"

# CSV檔案的欄位順序
csv_columns = ['SERIAL_NUMBER', 'ROOM_AGE', 'BUILDING_SHIFTING_AREA_SQUARE_METER', 'MAIN_USE',
               'MAIN_BUILDING_MATERIALS', 'CONSTRUCTION_COMPLETES_DATE', 'TOTAL_LAYER', 'ADDITIONAL_FEATURES']

try:
    # 連線到資料庫
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # 遍歷資料來源資料夾中的每一個資料夾
    for folder in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder)

        # 找到以 build 結尾的 CSV 檔案
        csv_files = glob.glob(os.path.join(folder_path, "*_build.csv"))

        for csv_file in csv_files:
            # 確定表格名稱，使用資料夾名稱
            table_name = f'build_{folder}'

            with open(csv_file, 'r', encoding='utf-8') as file:
                # 讀取 CSV 檔案中的資料
                next(file)  # 跳過 CSV 標題行
                next(file)  # 跳過 CSV 標題行
                for line in file:
                    data = line.strip().split(',')
                    # 將所有的 None 值轉換為空字串
                    data_dict = {
                        column: value if value else '' for column, value in zip(csv_columns, data)}
                    # 提取日期中的數字部分
                    raw_date = data_dict['CONSTRUCTION_COMPLETES_DATE']
                    matches = re.findall(r'\d+', raw_date)  # 提取字串中的所有數字
                    if len(matches) >= 3:
                        # 如果找到了至少三個數字，假設它們是年、月、日
                        year, month, day = map(int, matches[:3])
                        # 將西元年份轉換為四位數字
                        if year < 100:
                            year += 1911
                        # 檢查月份和日期是否在有效範圍內
                        if 1 <= month <= 12 and 1 <= day <= 31:
                            # 建立日期物件
                            date_obj = datetime(year, month, day)
                            # 將日期物件轉換為 'YYYY-MM-DD' 格式
                            formatted_date = date_obj.strftime('%Y-%m-%d')
                            data_dict['CONSTRUCTION_COMPLETES_DATE'] = formatted_date
                        else:
                            # 月份或日期不在有效範圍內，將日期設為空字串
                            data_dict['CONSTRUCTION_COMPLETES_DATE'] = ''
                    else:
                        # 如果找不到足夠的數字，將日期設為空字串
                        data_dict['CONSTRUCTION_COMPLETES_DATE'] = ''

                    # 檢查表格是否已存在的查詢語句
                    table_exists_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
                    cursor.execute(table_exists_query)
                    table_exists = cursor.fetchone()[0]

                    if not table_exists:
                        # 如果表格不存在，創建表格的SQL語句
                        create_table_query = f'''
                            CREATE TABLE {table_name} (
                                SERIAL_NUMBER VARCHAR(255) PRIMARY KEY,
                                ROOM_AGE VARCHAR(255),
                                BUILDING_SHIFTING_AREA_SQUARE_METER DOUBLE PRECISION,
                                MAIN_USE VARCHAR(255),
                                MAIN_BUILDING_MATERIALS VARCHAR(255),
                                CONSTRUCTION_COMPLETES_DATE VARCHAR(255),
                                TOTAL_LAYER VARCHAR(255),
                                ADDITIONAL_FEATURES VARCHAR(255)
                            );
                        '''
                        # 創建表格
                        cursor.execute(create_table_query)

                    # 插入或更新資料到表格中的SQL語句
                        # 插入或更新資料到表格中的SQL語句
                    insert_update_query = f'''
                        INSERT INTO {table_name} (SERIAL_NUMBER, ROOM_AGE, BUILDING_SHIFTING_AREA_SQUARE_METER, MAIN_USE, MAIN_BUILDING_MATERIALS, CONSTRUCTION_COMPLETES_DATE, TOTAL_LAYER, ADDITIONAL_FEATURES)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (SERIAL_NUMBER) DO UPDATE
                        SET (ROOM_AGE, BUILDING_SHIFTING_AREA_SQUARE_METER, MAIN_USE, MAIN_BUILDING_MATERIALS, CONSTRUCTION_COMPLETES_DATE, TOTAL_LAYER, ADDITIONAL_FEATURES)
                        = (EXCLUDED.ROOM_AGE, EXCLUDED.BUILDING_SHIFTING_AREA_SQUARE_METER, EXCLUDED.MAIN_USE, EXCLUDED.MAIN_BUILDING_MATERIALS, EXCLUDED.CONSTRUCTION_COMPLETES_DATE, EXCLUDED.TOTAL_LAYER, EXCLUDED.ADDITIONAL_FEATURES);
                    '''

                    # 執行插入或更新資料的SQL語句
                    cursor.execute(insert_update_query, (
                        data_dict['SERIAL_NUMBER'], int(data_dict['ROOM_AGE']), float(
                            data_dict['BUILDING_SHIFTING_AREA_SQUARE_METER']),
                        data_dict['MAIN_USE'], data_dict['MAIN_BUILDING_MATERIALS'], data_dict[
                            'CONSTRUCTION_COMPLETES_DATE'], data_dict['TOTAL_LAYER'], data_dict['ADDITIONAL_FEATURES']
                    ))

                print(f"Data from {csv_file} imported/updated successfully.")

    # 提交變更
    connection.commit()

except (Exception, psycopg2.Error) as error:
    print("Error:", error)

finally:
    # 關閉cursor和連線
    if cursor:
        cursor.close()
    if connection:
        connection.close()
