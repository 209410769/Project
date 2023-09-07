import pandas as pd
import psycopg2
import os

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构建 CSV 文件的完整路径
csv_file = os.path.join(script_dir, 'data', '2023-08-04 22-09',
                        'RVR', 'real_estate1021', 'a_lvr_land_a.csv')

# 读取 CSV 文件
data = pd.read_csv(csv_file)

selected_columns = [
    '鄉鎮市區',
    '交易標的',
    '交易年月日',
    '總價元',
    '單價元平方公尺',
    '建物型態',
    '主要用途',
    '建築完成年月',
    '主建物面積',
    '車位類別'
]

data = data[selected_columns]

# 设置数据库连接参数
db_params = {
    'dbname': 'postgres',  # 替换为您的数据库名称
    'user': 'postgres',        # 替换为您的数据库用户名
    'password': '0000',  # 替换为您的数据库密码
    'host': 'localhost',        # 数据库服务器主机
    'port': 5433                # 数据库服务器端口
}

# 建立数据库连接
conn = psycopg2.connect(**db_params)

# 创建一个游标对象
cur = conn.cursor()

# 检查表是否存在
table_name = 'A_RVR'  # 替换为您的目标表名称
cur.execute(
    f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
table_exists = cur.fetchone()[0]

if not table_exists:
    # 如果表不存在，则创建表
    create_table_query = f"""
    CREATE TABLE {table_name} (
        鄉鎮市區 VARCHAR(255),
        交易標的 VARCHAR(255),
        交易年月日 DATE,
        總價元 INT,
        單價元平方公尺 FLOAT,
        建物型態 VARCHAR(255),
        主要用途 VARCHAR(255),
        建築完成年月 DATE,
        主建物面積 FLOAT,
        車位類別 VARCHAR(255)
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    print(f"Table '{table_name}' created.")
else:
    print(f"Table '{table_name}' already exists.")

# 将数据逐行插入到数据库表
for index, row in data.iterrows():
    insert_query = f"INSERT INTO {table_name} ({', '.join(selected_columns)}) VALUES {tuple(row)};"
    cur.execute(insert_query)

# 提交事务并关闭连接
conn.commit()
cur.close()
conn.close()
