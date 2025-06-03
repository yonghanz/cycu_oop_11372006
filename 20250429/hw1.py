import csv
from bs4 import BeautifulSoup

def extract_bus_info(html_content, route_name):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 搜尋指定的公車路線名稱
    routes = soup.find_all('a', class_='route-link')  # 根據實際 HTML 調整
    for route in routes:
        if route_name in route.text.strip():
            route_url = route['href']
            print(f"找到路線: {route.text.strip()}, 路徑: {route_url}")

            # 模擬進入該路線的詳細資訊頁面
            # 假設車站資訊在同一頁面中，直接提取車站名稱
            stations = soup.find_all('div', class_='station-name')  # 根據實際 HTML 調整
            station_names = [station.text.strip() for station in stations]
            print("車站名稱列表:")
            for name in station_names:
                print(name)
            return

    print(f"找不到路線名稱為 {route_name} 的公車路線。")

def extract_all_bus_routes(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 搜尋所有公車路線
    routes = soup.find_all('a', class_='route-link')  # 根據實際 HTML 調整
    if not routes:
        print("找不到任何公車路線。")
        return

    print("所有公車路線代碼與名稱：")
    for route in routes:
        route_name = route.text.strip()
        route_url = route.get('href', '無路徑')
        print(f"路線名稱: {route_name}, 路徑: {route_url}")

def extract_all_bus_routes_to_csv(html_content, output_file):
    soup = BeautifulSoup(html_content, 'html.parser')

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

# 測試範例
route_name = input("請輸入公車路線名稱：")
output_file = "bus_routes.csv"  # 輸出的 CSV 檔案名稱
with open("視覺化大眾運輸地圖 - 巴視達.html", "r", encoding="utf-8") as file:
    html_content = file.read()
    extract_bus_info(html_content, route_name)
    extract_all_bus_routes(html_content)
    extract_all_bus_routes_to_csv(html_content, output_file)