import os
import pandas as pd
file_path = './code/data/2023-09-02 17-09/RVR/real_estate1021/a_lvr_land_a.csv'
# 用pd.read_csv()加载CSV文件到DataFrame
df = pd.read_csv(file_path)

# 显示DataFrame的前几行数据
print(df.head())
