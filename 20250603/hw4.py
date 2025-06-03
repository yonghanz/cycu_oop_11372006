# -*- coding: utf-8 -*-
"""
This module retrieves bus stop data for a specific route and direction from the Taipei eBus website,
saves the rendered HTML and CSV file.
"""
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup


class taipei_route_info:
    """
    Manages fetching, parsing, and storing bus stop data for a specified route and direction.
    """
    def __init__(self, route_id: str, working_directory: str = 'data'):
        self.route_id = route_id
        self.direction = 'come'  # 強制設定為回程
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
            print(f"Response content: {response.text}")
            raise Exception(f"Failed to fetch HTML for route {self.route_id}. Status code: {response.status_code}")

    def parse_stations(self) -> list:
        """
        Parses station names from the HTML content for the specified route and direction.
        """
        soup = BeautifulSoup(self.content, 'html.parser')
        
        # 尋找回程資料區塊
        route_div = soup.find('div', id='BackDirectionRoute')

        if not route_div:
            print(f"❌ No route data found for direction 'come'.")
            return []

        # 提取車站名稱
        station_names = []
        for station in route_div.find_all('span', class_='auto-list-stationlist-place'):
            station_names.append(station.text.strip())

        return station_names

    def export_bus_stations_to_csv(self, output_csv: str):
        """
        Exports station names for the specified route and direction to a CSV file.

        Args:
            output_csv (str): The path to the output CSV file.
        """
        station_names = self.parse_stations()
        if not station_names:
            print(f"No station data found for route {self.route_id} in direction 'come'.")
            return

        # Save station names to CSV
        df = pd.DataFrame(station_names, columns=["StationName"])
        df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print(f"✅ Saved station names to {output_csv}")


if __name__ == "__main__":
    # 輸入公車 ID
    bus_id = input("請輸入公車 ID: ").strip()

    # 初始化 taipei_route_info 並匯出回程站點資料
    route_info = taipei_route_info(route_id=bus_id)
    
    # 指定輸出 CSV 檔案路徑
    output_csv_path = f"c:/Users/User/Desktop/cycu_oop_11372006/20250603/{bus_id}_come_stations.csv"
    route_info.export_bus_stations_to_csv(output_csv=output_csv_path)