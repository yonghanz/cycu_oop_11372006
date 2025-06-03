import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import folium
import pandas as pd
from sqlalchemy import create_engine
from folium.features import CustomIcon

def fetch_all_bus_routes(url, output_file):
    """
    使用 requests 爬取公車路線資料，並儲存為 CSV 檔案。
    """
    try:
        # 發送 GET 請求到網站
        response = requests.get(url)
        response.raise_for_status()  # 確保請求成功
        soup = BeautifulSoup(response.text, 'html.parser')

        # 搜尋所有公車路線
        routes = soup.find_all('a', class_='route-link')  # 根據實際 HTML 調整
        if not routes:
            print("找不到任何公車路線。")
            return

        # 將路線名稱與代碼寫入 CSV 檔案
        with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['路線名稱', '路徑'])  # 寫入標題

            for route in routes:
                route_name = route.text.strip()
                route_url = route.get('href', '無路徑')
                writer.writerow([route_name, route_url])  # 寫入每一行
                print(f"路線名稱: {route_name}, 路徑: {route_url}")

        print(f"所有公車路線已儲存至 {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"無法連接到網站：{e}")

def fetch_all_bus_routes_with_selenium(url, output_file):
    """
    使用 Selenium 爬取公車路線資料，並儲存為 CSV 檔案。
    """
    # 設定 ChromeDriver 路徑
    driver = webdriver.Chrome()  # 確保已安裝 ChromeDriver
    driver.get(url)

    try:
        time.sleep(5)  # 等待頁面載入

        # 搜尋所有公車路線
        routes = driver.find_elements(By.CLASS_NAME, "route-link")  # 根據實際 HTML 調整
        if not routes:
            print("找不到任何公車路線。")
            return

        # 將路線名稱與代碼寫入 CSV 檔案
        with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['路線名稱', '路徑'])  # 寫入標題

            for route in routes:
                route_name = route.text.strip()
                route_url = route.get_attribute('href')
                writer.writerow([route_name, route_url])  # 寫入每一行
                print(f"路線名稱: {route_name}, 路徑: {route_url}")

        print(f"所有公車路線已儲存至 {output_file}")

    finally:
        driver.quit()

def plot_station_with_icon(stop_id, working_directory='data', icon_path='火柴人.png'):
    """
    根據車站號碼繪製地圖，顯示該車站的位置，並使用自定義圖示。

    Args:
        stop_id (str): 車站號碼。
        working_directory (str): SQLite 資料庫所在的目錄。
        icon_path (str): 自定義圖示的檔案路徑。
    """
    # 連接到 SQLite 資料庫
    db_file = f"{working_directory}/hermes_ebus_taipei.sqlite3"
    engine = create_engine(f"sqlite:///{db_file}")

    # 從資料庫中查詢車站資訊
    query = f"""
    SELECT stop_name, latitude, longitude, route_id, direction
    FROM data_route_info_busstop
    WHERE stop_id = '{stop_id}'
    """
    station_data = pd.read_sql(query, engine)

    if station_data.empty:
        print(f"找不到車站號碼為 {stop_id} 的資料。")
        return

    # 提取車站資訊
    stop_name = station_data.iloc[0]['stop_name']
    latitude = station_data.iloc[0]['latitude']
    longitude = station_data.iloc[0]['longitude']
    route_id = station_data.iloc[0]['route_id']
    direction = station_data.iloc[0]['direction']

    print(f"車站名稱: {stop_name}, 緯度: {latitude}, 經度: {longitude}, 路線: {route_id}, 方向: {direction}")

    # 繪製地圖
    map_center = [latitude, longitude]
    m = folium.Map(location=map_center, zoom_start=15)

    # 自定義圖示
    icon = CustomIcon(
        icon_image=icon_path,
        icon_size=(50, 50)  # 調整圖示大小
    )

    # 在地圖上添加標記
    folium.Marker(
        location=map_center,
        popup=f"車站名稱: {stop_name}<br>路線: {route_id}<br>方向: {direction}",
        tooltip=stop_name,
        icon=icon
    ).add_to(m)

    # 保存地圖為 HTML
    map_file = f"{working_directory}/station_{stop_id}_map_with_icon.html"
    m.save(map_file)
    print(f"地圖已儲存至 {map_file}")

    # 返回地圖物件（可選）
    return m

if __name__ == "__main__":
    # 使用範例
    url = "https://bus.pcrest.tw/"
    output_file = "bus_routes.csv"
    fetch_all_bus_routes_with_selenium(url, output_file)

    # 輸入車站號碼
    stop_id = input("請輸入車站號碼：")
    plot_station_with_icon(stop_id, icon_path='火柴人.png')