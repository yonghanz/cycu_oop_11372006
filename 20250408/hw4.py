# -*- coding: utf-8 -*-
import csv
from playwright.sync_api import sync_playwright


class BusRouteInfo:
    def __init__(self, routeid: str, direction: str = 'go'):
        self.rid = routeid
        self.direction = direction
        self.url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={routeid}'
        self.rows = []

        if direction not in ['go', 'come']:
            raise ValueError("方向必須為 'go' 或 'come'")

        self._fetch_via_playwright()

    def _fetch_via_playwright(self):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)  # 設定為 False 以便觀察操作過程
                page = browser.new_page()
                page.goto(self.url)

                # 等待頁面完全加載
                page.wait_for_load_state("load")  # 等待頁面完全加載完成
                print("頁面載入完成，開始抓取資料...")

                # 切換方向（回程）
                if self.direction == 'come':
                    page.click('a.stationlist-come-go-gray.stationlist-come')

                # 增加等待時間
                try:
                    page.wait_for_selector("table tbody tr", timeout=60000)  # 增加超時時間至 60 秒
                except TimeoutError:
                    print("❌ 等待資料超時，無法找到站點資料")
                    return

                rows = page.query_selector_all("table tbody tr")
                if not rows:
                    print("❌ 無法找到任何站點資料，可能網頁結構改變")
                    return

                for row in rows:
                    cols = row.query_selector_all("td")
                    if len(cols) < 6:
                        continue

                    arrival_info = cols[0].inner_text().strip()
                    stop_number = cols[1].inner_text().strip()
                    stop_name = cols[2].inner_text().strip()
                    stop_id = cols[3].inner_text().strip()
                    latitude = cols[4].inner_text().strip()
                    longitude = cols[5].inner_text().strip()

                    self.rows.append([arrival_info, stop_number, stop_name, stop_id, latitude, longitude])

                browser.close()

        except Exception as e:
            print(f"❌ 撈取資料時發生錯誤：{e}")

    def save_to_csv(self, filename="bus_route_info.csv"):
        if not self.rows:
            print("❌ 無法儲存，沒有任何站牌資料")
            return

        with open(filename, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["arrival_info", "stop_number", "stop_name", "stop_id", "latitude", "longitude"])
            writer.writerows(self.rows)

        print(f"✅ 成功儲存資料到 {filename}")


# 主程式
if __name__ == "__main__":
    route_id = input("請輸入公車代碼（例如 '0100000A00'）：").strip()
    direction = input("請輸入方向（'go' 或 'come'，預設為 'go'）：").strip() or 'go'

    bus = BusRouteInfo(routeid=route_id, direction=direction)
    bus.save_to_csv()
