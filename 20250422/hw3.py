from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import geopandas as gpd
from shapely.geometry import Point
import folium
import matplotlib
import matplotlib.pyplot as plt

# 關閉 matplotlib 的互動模式
matplotlib.use('Agg')


def fetch_bus_stops_with_selenium(route_name):
    """
    使用 Selenium 從網站抓取指定公車路線的站點資料
    :param route_name: 公車路線名稱
    :return: 包含站點名稱和經緯度的 GeoDataFrame
    """
    # 設定 ChromeDriver 路徑
    service = Service("C:/Users/User/Desktop/chromedriver.exe")  # 替換為你的 ChromeDriver 路徑
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 啟用無頭模式
    driver = webdriver.Chrome(service=service, options=options)

    # 開啟目標網站
    url = "https://bus.pcrest.tw/Menu/"
    driver.get(url)

    # 等待頁面載入完成
    driver.implicitly_wait(10)

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 假設站點資料在特定的 HTML 標籤中，根據實際網站結構調整
    stops = []
    for stop in soup.find_all('div', class_='stop-class'):  # 替換為正確的標籤和 class
        stop_name = stop.find('span', class_='stop-name').text.strip()
        lat = float(stop['data-lat'])  # 假設經緯度在 data-lat 和 data-lon 屬性中
        lon = float(stop['data-lon'])
        stops.append({'name': stop_name, 'latitude': lat, 'longitude': lon})

    # 關閉瀏覽器
    driver.quit()

    # 將資料轉換為 GeoDataFrame
    gdf = gpd.GeoDataFrame(
        stops,
        geometry=[Point(stop['longitude'], stop['latitude']) for stop in stops],
        crs="EPSG:4326"
    )
    return gdf


# 測試程式
if __name__ == "__main__":
    route_name = input("請輸入公車路線名稱：")
    gdf = fetch_bus_stops_with_selenium(route_name)

    if gdf is not None and not gdf.empty:
        print(gdf.head())
    else:
        print(f"找不到公車路線名稱 {route_name} 的站點資料。")