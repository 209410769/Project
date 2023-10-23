import os
import requests
import zipfile
import time
from urllib3.exceptions import ConnectTimeoutError
from tqdm import tqdm

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


# 資料存放的基本路徑
base_path = "code/data"
zip_folder_path = os.path.join(base_path, 'RVR_ZIP')
output_folder_path = os.path.join(base_path, 'RVR')  # 保存解壓縮檔案的資料夾


def real_estate_crawler(year, season):
    if year > 1000:
        year -= 1911

    if not os.path.isdir(zip_folder_path):
        os.makedirs(zip_folder_path)

    # 下載不動產 zip 檔案
    res = requests.get("https://plvr.land.moi.gov.tw//DownloadSeason?season=" +
                       str(year) + "S" + str(season) + "&type=zip&fileName=lvr_landcsv.zip")

    # 儲存檔案內容到指定位置
    fname = f"{year}{season}.zip"
    file_path = os.path.join(zip_folder_path, fname)

    # 判斷檔案是否存在，如果存在則刪除
    if os.path.exists(file_path):
        os.remove(file_path)

    open(file_path, 'wb').write(res.content)

    # 解壓縮檔案到資料夾中
    output_folder = os.path.join(
        output_folder_path, f"real_estate_{year}{season}")
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)  # 如果資料夾不存在，則建立

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

    time.sleep(10)


for year in tqdm(range(102, 110), desc="Processing Years"):
    for season in range(1, 5):
        print('crawl ', year, 'Q', season)
        real_estate_crawler_with_retry(year, season)
