import pandas as pd
import requests
import os
import zipfile
import time

from urllib3.exceptions import ConnectTimeoutError

from tqdm import tqdm  # 引入 tqdm
retry_interval = 50
def real_estate_crawler_with_retry(year, season, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            real_estate_crawler(year, season)
            break  # 若連接成功，退出循環
        except (ConnectTimeoutError, requests.exceptions.Timeout):
            print("連接超時，等待一段時間後重試...")
            time.sleep(retry_interval)
            retries += 1
    else:
        print("無法建立連接，已超過最大重試次數。")

from datetime import datetime
current_datetime = datetime.now()
current_date = current_datetime.date()  # 獲取日期部分
current_time = current_datetime.time()  # 獲取時間部分
# 將日期和時間轉換為字符串
date_string = current_date.strftime("%Y-%m-%d")
time_string = current_time.strftime("%H-%M")  # 使用橫線替代冒號
# # 父資料夾名稱
base_path = "RVR"

# parent_folder = os.path.join(base_path, date_string + " " + time_string, 'RVR')
parent_folder = os.path.join(base_path, date_string + " " + time_string, 'RVR')
print(parent_folder)
# zip_folder_path = os.path.join(base_path, date_string + " " + time_string, 'RVR_ZIP')
zip_folder_path = os.path.join(base_path, date_string + " " + time_string, 'RVR_ZIP')
print(zip_folder_path)

def real_estate_crawler(year, season):
    if year > 1000:
        year -= 1911

    if not os.path.isdir(zip_folder_path):
        os.makedirs(zip_folder_path)

    # 下載不動產 zip 檔案
    res = requests.get("https://plvr.land.moi.gov.tw//DownloadSeason?season=" +
                       str(year) + "S" + str(season) + "&type=zip&fileName=lvr_landcsv.zip")

    # 儲存檔案內容到指定位置
    fname = str(year) + str(season) + '.zip'
    file_path = os.path.join(zip_folder_path, fname)
    open(file_path, 'wb').write(res.content)

    # 建立資料夾用於存放解壓縮檔案
    folder = 'real_estate' + str(year) + str(season)
    next_folder = os.path.join(parent_folder, folder)
    if not os.path.isdir(parent_folder):
        os.makedirs(next_folder)  # 使用 os.makedirs() 建立資料夾

    # 解壓縮檔案到資料夾中
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(next_folder)

    time.sleep(10)


for year in tqdm(range(102, 110), desc="Processing Years"):
    for season in range(1, 5):
        print('crawl ', year, 'Q', season)
        real_estate_crawler_with_retry(year, season)
