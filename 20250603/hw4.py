# -*- coding: utf-8 -*-
import os
import re
import json
import pandas as pd
import requests

class TaipeiRouteInfo:
    def __init__(self, route_id: str, direction: str = 'go', working_directory: str = 'data'):
        self.route_id = route_id
        self.direction = direction
        self.working_directory = working_directory
        self.url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}'

        if self.direction not in ['go', 'come']:
            raise ValueError("Direction must be 'go' or 'come'")
        
        # 檔案路徑
        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)

        self.html_file = f"{self.working_directory}/ebus_taipei_{self.route_id}.html"

        # 如果檔案不存在，從網頁下載
        if not os.path.exists(self.html_file):
            print(f"🔍 下載 HTML: {self.url}")
            response = requests.get(self.url)
            if response.status_code == 200:
                with open(self.html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"✅ 已儲存為 {self.html_file}")
            else:
                raise Exception(f"❌ 無法下載 HTML，HTTP 狀態碼: {response.status_code}")

        # 讀取 HTML 內容
        with open(self.html_file, 'r', encoding='utf-8') as file:
            self.content = file.read()

    def extract_stops(self):
        """
        擷取站點資料（分去程或回程）
        """
        pattern = r'JSON\.stringify\s*\(\s*(\{[\s\S]*?\})\s*\)'
        match = re.search(pattern, self.content)
        if not match:
            raise Exception("❌ 無法解析 JSON 資料")

        json_text = match.group(1)
        data = json.loads(json_text)

        # 擷取 direction 資料：goStops 或 comeStops
        stops_key = 'goStops' if self.direction == 'go' else 'comeStops'
        stops = data.get(stops_key, [])

        stop_list = []
        for stop in stops:
            stop_list.append({
                'StopID': stop.get('StopID', ''),
                'StopName': stop.get('StopName', ''),
                'StopSeq': stop.get('StopSeq', ''),
                'RouteName': data.get('routename', ''),
                'Direction': '去程' if self.direction == 'go' else '回程'
            })
        return stop_list


if __name__ == "__main__":
    route_id = input("請輸入公車代碼（如 0162003400）：").strip()

    all_stops = []

    try:
        for direction in ['go', 'come']:
            route = TaipeiRouteInfo(route_id=route_id, direction=direction)
            stops = route.extract_stops()
            all_stops.extend(stops)

            df = pd.DataFrame(stops)
            dir_label = 'go' if direction == 'go' else 'come'
            csv_path = f"data/{route_id}_{dir_label}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"✅ 已儲存 {len(df)} 筆「{df.iloc[0]['Direction']}」資料至：{csv_path}")

    except Exception as e:
        print(f"❌ 錯誤發生: {e}")
