import pandas as pd
import os

# 定义数据存放的路径
folder_path = "code/data/2023-10-09 17-25/RVR/real_estate1021"

# 获取文件夹中所有 CSV 文件
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# 初始化一个空的 DataFrame 用于存储数据
all_data_df = pd.DataFrame()

# 将所有 CSV 文件的数据加载到 DataFrame
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)
    # 使用concat方法合并DataFrame
    all_data_df = pd.concat([all_data_df, df], ignore_index=True)

# 在这里进行进一步的数据处理和分析

# 将DataFrame保存为CSV文件
output_csv_path = "output_data.csv"  # 指定保存的文件路径
all_data_df.to_csv(output_csv_path, index=False)  # 将DataFrame保存为CSV文件，不保存行索引

print(f"数据已保存至 {output_csv_path}")
