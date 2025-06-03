# -*- coding: utf-8 -*-
"""
This script retrieves bus stop data for all route IDs listed in route_name_code.csv,
fetches the "go" direction stops, and saves all routes' stops to a single CSV file in a horizontal format.
"""
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup


class taipei_route_info:
    """
    Manages fetching, parsing, and storing bus stop data for a specified route and direction.
    """
    def __init__(self, route_id: str, direction: str = 'go', working_directory: str = 'data'):
        self.route_id = route_id
        self.direction = direction
        self.content = None
        self.url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}'
        self.working_directory = working_directory
        self.html_file = f"{self.working_directory}/ebus_taipei_{self.route_id}.html"

        # 確保資料夾存在
        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)
            print(f"✅ Created working directory: {self.working_directory}")

        # 如果檔案不存在，抓取 HTML
        if not os.path.exists(self.html_file):
            self.fetch_html()

        # 讀取 HTML 檔案
        with open(self.html_file, 'r', encoding='utf-8') as file:
            self.content = file.read()

    def fetch_html(self):
        """
        Fetches the HTML content for the specified route ID and saves it to a file.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            with open(self.html_file, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"✅ Fetched and saved HTML for route {self.route_id}")
        else:
            print(f"❌ Failed to fetch HTML for route {self.route_id}. Status code: {response.status_code}")
            raise Exception(f"Failed to fetch HTML for route {self.route_id}. Status code: {response.status_code}")

    def parse_stations(self) -> list:
        """
        Parses station names from the HTML content for the specified route and direction.
        """
        soup = BeautifulSoup(self.content, 'html.parser')
        
        # 根據方向選擇正確的區塊
        if self.direction == 'go':
            route_div = soup.find('div', id='GoDirectionRoute')
        else:
            raise ValueError("This script only supports 'go' direction.")

        if not route_div:
            print(f"❌ No route data found for direction {self.direction}.")
            return []

        # 提取車站名稱
        station_names = []
        for station in route_div.find_all('span', class_='auto-list-stationlist-place'):
            station_names.append(station.text.strip())

        return station_names


if __name__ == "__main__":
    # 讀取 route_name_code.csv
    csv_file_path = "c:/Users/User/Desktop/cycu_oop_11372006/data/route_name_code.csv"
    output_csv_path = "c:/Users/User/Desktop/cycu_oop_11372006/20250603/all_routes_horizontal.csv"

    # 確保輸出目錄存在
    output_directory = os.path.dirname(output_csv_path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 讀取 CSV 檔案
    route_data = pd.read_csv(csv_file_path, header=None, names=["RouteName", "RouteID"], encoding="utf-8-sig")

    # 初始化一個空的列表，用於存放所有路線的資料
    all_routes_data = []

    # 遍歷每個公車代碼
    for _, row in route_data.iterrows():
        route_name = row["RouteName"]
        route_id = row["RouteID"]

        print(f"🔍 正在處理公車路線: {route_name} (ID: {route_id})")

        try:
            # 初始化 taipei_route_info 並抓取站點資料
            route_info = taipei_route_info(route_id=route_id, direction="go", working_directory="data")
            station_names = route_info.parse_stations()

            # 如果有站點資料，將其加入到列表
            if station_names:
                row_data = [route_name, route_id] + station_names
                all_routes_data.append(row_data)
            else:
                print(f"❌ No station data found for route {route_name} (ID: {route_id})")
        except Exception as e:
            print(f"❌ 無法處理公車路線 {route_name} (ID: {route_id})，錯誤: {e}")

    # 將所有路線的資料轉換為 DataFrame
    max_columns = max(len(row) for row in all_routes_data)  # 找出最多的站點數量
    column_names = ["RouteName", "RouteID"] + [f"Station{i}" for i in range(1, max_columns - 1)]
    all_routes_df = pd.DataFrame(all_routes_data, columns=column_names)

    # 將所有路線的資料保存到單一的 CSV 檔案
    all_routes_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"✅ 所有路線的站點資料已保存到 {output_csv_path}")
