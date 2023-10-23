# import psycopg2
# import csv
# from datetime import datetime

# # 資料庫連線參數
# db_params = {
#     'host': 'localhost',
#     'database': 'postgres',
#     'user': 'postgres',
#     'password': '0000',
#     'port': '5432'
# }

# # 資料庫中的表格名稱
# table_name = 'test_for_build_table'

# # CSV檔案路徑
# csv_file_path = '/Users/jimmy/Desktop/Jimmy/Project/code/data/RVR/real_estate_1021/a_lvr_land_a_build.csv'

# try:
#     # 連線到資料庫
#     connection = psycopg2.connect(**db_params)
#     cursor = connection.cursor()

#     # 檢查表格是否存在的SQL查詢
#     table_exists_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
#     cursor.execute(table_exists_query)
#     table_exists = cursor.fetchone()[0]

#     if not table_exists:
#         # 如果表格不存在，創建表格的SQL語句
#         create_table_query = f'''
#             CREATE TABLE {table_name} (
# ID SERIAL PRIMARY KEY,
# SERIAL_NUMBER VARCHAR(255),
# ROOM_AGE INTEGER,
# BUILDING_SHIFTING_AREA_SQUARE_METER DOUBLE PRECISION,
# MAIN_USE VARCHAR(255),
# MAIN_BUILDING_MATERIALS VARCHAR(255),
# CONSTRUCTION_COMPLETES_DATE DATE,
# TOTAL_LAYER VARCHAR(255),
# ADDITIONAL_FEATURES VARCHAR(255)
#             );
#         '''
#         # 創建表格
#         cursor.execute(create_table_query)

#     # 開啟CSV檔案並讀取資料
#     with open(csv_file_path, 'r', encoding='utf-8') as file:
#         csv_reader = csv.reader(file)
#         next(csv_reader)  # 跳過標題行

#         for row in csv_reader:
#             # 將CSV檔案中的資料映射到變數
#             serial_number = row[0]
#             room_age = int(row[1]) if row[1].isdigit() else None
#             # 檢查 'building shifting area square meter' 是否為有效的浮點數字串
#             area = float(row[2]) if row[2].replace(
#                 '.', '', 1).isdigit() else None
#             main_use = row[3] if row[3] else None
#             main_materials = row[4] if row[4] else None
#             completion_date = row[5] if row[5] else None  # 日期格式需確認與轉換
#             total_layers = row[6] if row[6] else None  # 這裡的格式需確認與轉換
#             additional_features = row[7] if row[7] else None

#             # 處理日期格式
#             if completion_date:
#                 try:
#                     # 解析 "89年11月22日" 格式的日期
#                     date_obj = datetime.strptime(completion_date, '%y年%m月%d日')
#                     # 轉換為 "YYYY-MM-DD" 格式
#                     formatted_date = date_obj.strftime('%Y-%m-%d')
#                 except ValueError:
#                     # 處理無效日期格式的情況
#                     formatted_date = None
#             else:
#                 formatted_date = None

#             # 插入資料到資料庫中
#             insert_query = '''
#                 INSERT INTO test_for_build_table (SERIAL_NUMBER, ROOM_AGE, BUILDING_SHIFTING_AREA_SQUARE_METER, MAIN_USE, MAIN_BUILDING_MATERIALS, CONSTRUCTION_COMPLETES_DATE, TOTAL_LAYER, ADDITIONAL_FEATURES)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                 '''

# # 在執行插入資料的SQL語句時，不需要指定id欄位的值
#             cursor.execute(insert_query, (serial_number, room_age, area, main_use,
#                                           main_materials, completion_date, total_layers, additional_features))

#         print("Data imported successfully.")

#     # 提交變更
#     connection.commit()

# except (Exception, psycopg2.Error) as error:
#     print("Error:", error)

# finally:
#     # 關閉cursor和連線
#     if cursor:
#         cursor.close()
#     if connection:
#         connection.close()
import pandas as pd
import psycopg2
import csv
# 讀取 CSV 檔案為 DataFrame
csv_file_path = '/Users/jimmy/Desktop/Jimmy/Project/code/data/RVR/real_estate_1021/a_lvr_land_a_build.csv'
df = pd.read_csv(csv_file_path, encoding='utf-8')

# 將 DataFrame 欄位名稱重新命名為指定順序
new_column_order = ['SERIAL_NUMBER', 'ROOM_AGE', 'BUILDING_SHIFTING_AREA_SQUARE_METER', 'MAIN_USE',
                    'MAIN_BUILDING_MATERIALS', 'CONSTRUCTION_COMPLETES_DATE', 'TOTAL_LAYER', 'ADDITIONAL_FEATURES']
df = df.rename(columns=dict(zip(df.columns, new_column_order)))
# 刪除第 0 筆資料（索引為 0）
df = df.drop(0)
# 重新設定索引（可選步驟）
df = df.reset_index(drop=True)
# 將日期欄位轉換為 'YYYY-MM-DD' 格式，遇到無法轉換的日期設為 NaT
df['CONSTRUCTION_COMPLETES_DATE'] = pd.to_datetime(
    df['CONSTRUCTION_COMPLETES_DATE'], format='%Y年%m月%d日', errors='coerce')

# 刪除日期轉換失敗的資料（NaT 表示轉換失敗）
df = df.dropna(subset=['CONSTRUCTION_COMPLETES_DATE'])

# 將日期欄位轉換為 'YYYY-MM-DD' 字符串
df['CONSTRUCTION_COMPLETES_DATE'] = df['CONSTRUCTION_COMPLETES_DATE'].dt.strftime(
    '%Y-%m-%d')
# 這時候 DataFrame 的欄位名稱就是你指定的順序了
print(df.head())


# # 資料庫連線參數
# db_params = {
#     'host': 'localhost',
#     'database': 'postgres',
#     'user': 'postgres',
#     'password': '0000',
#     'port': '5432'
# }

# # 資料庫中的表格名稱
# table_name = 'test_for_build_table'

# # 創建表格的SQL語句
# create_table_query = f'''
#     CREATE TABLE IF NOT EXISTS {table_name} (
#         SERIAL_NUMBER VARCHAR(255),
#         ROOM_AGE INTEGER,
#         BUILDING_SHIFTING_AREA_SQUARE_METER DOUBLE PRECISION,
#         MAIN_USE VARCHAR(255),
#         MAIN_BUILDING_MATERIALS VARCHAR(255),
#         CONSTRUCTION_COMPLETES_DATE DATE,
#         TOTAL_LAYER VARCHAR(255),
#         ADDITIONAL_FEATURES VARCHAR(255)
#     );
# '''

# try:
#     # 連線到資料庫
#     connection = psycopg2.connect(**db_params)
#     cursor = connection.cursor()

#     # 執行創建表格的SQL指令
#     cursor.execute(create_table_query)
#     connection.commit()  # 提交變更

#     # 以下是插入資料的程式碼，放在創建表格的SQL指令之後

#     # 開啟CSV檔案並讀取資料
#     with open(csv_file_path, 'r', encoding='utf-8') as file:
#         csv_reader = csv.reader(file)
#         next(csv_reader)  # 跳過標題行

#         # 插入資料到資料庫中
#         for row in csv_reader:
#             # 將CSV檔案中的資料映射到變數，然後執行插入資料的SQL語句
#             insert_query = '''
#                 INSERT INTO test_for_build_table (SERIAL_NUMBER, ROOM_AGE, BUILDING_SHIFTING_AREA_SQUARE_METER, MAIN_USE, MAIN_BUILDING_MATERIALS, CONSTRUCTION_COMPLETES_DATE, TOTAL_LAYER, ADDITIONAL_FEATURES)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             '''
#             cursor.execute(insert_query, (
#                 row[0],  # SERIAL_NUMBER
#                 int(row[1]) if row[1].isdigit() else None,  # ROOM_AGE
#                 float(row[2]) if row[2].replace('.', '', 1).isdigit(
#                 ) else None,  # BUILDING_SHIFTING_AREA_SQUARE_METER
#                 row[3],  # MAIN_USE
#                 row[4],  # MAIN_BUILDING_MATERIALS
#                 row[5],  # CONSTRUCTION_COMPLETES_DATE
#                 row[6],  # TOTAL_LAYER
#                 row[7]   # ADDITIONAL_FEATURES
#             ))

#         # 提交變更
#         connection.commit()
#         print("Data imported successfully.")

# except (Exception, psycopg2.Error) as error:
#     print("Error:", error)

# finally:
#     # 關閉cursor和連線
#     if cursor:
#         cursor.close()
#     if connection:
#         connection.close()
