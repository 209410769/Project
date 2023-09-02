import os
print("answer")
# 指定目錄路徑
directory = 'rvr'  # 請替換成您的實際目錄路徑

# 遍歷目錄
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            print(file_path)
