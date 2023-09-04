import psycopg2
data_path = './data/2023-08-04 22-09/RVR/real_estate1021/a_lvr_land_a.csv'
# # 设置数据库连接参数
# db_params = {
#     'dbname': 'PostgreSQL',
#     'user': 'postgres',
#     'password': '0000',
#     'host': 'localhost',  # 如果 PostgreSQL 位于本地，请使用 'localhost' 或 '127.0.0.1'
#     'port': 5433  # 指定端口号 5433
# }
# 连接到 PostgreSQL 数据库
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='0000',
    host='localhost',  # 数据库服务器主机
    port=5433          # 数据库服务器端口
)

# 创建一个游标对象
cur = conn.cursor()

# 定义创建表的 SQL 命令
create_table_sql = '''
    CREATE TABLE IF NOT EXISTS your_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        age INT
    )
'''

# 执行 SQL 命令以创建表
cur.execute(create_table_sql)

# 提交事务
conn.commit()

# 关闭游标和数据库连接
cur.close()
conn.close()
