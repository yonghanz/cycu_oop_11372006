import requests
import csv

def fetch_bus_data_to_csv(bus_route_id, filename="bus_route_info.csv"):
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={bus_route_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ 無法取得資料，伺服器返回狀態碼：", response.status_code)
        return

    try:
        data = response.json()
    except ValueError:
        print("❌ 無法解析伺服器返回的內容為 JSON 格式。")
        print("伺服器返回的內容：", response.text)
        return

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        # 寫入欄位名稱
        writer.writerow(["公車到達時間", "車站序號", "車站名稱", "車站編號", "latitude", "longitude"])

        for direction in data:  # 可能含去程、回程等
            for stop in direction.get("stops", []):
                arrival_info = stop.get("arrival_info", "無資料")
                stop_number = stop.get("stop_number", "")
                stop_name = stop.get("stop_name", {}).get("zh_tw", "")
                stop_id = stop.get("stop_id", "")
                lat = stop.get("position", {}).get("lat", "")
                lng = stop.get("position", {}).get("lng", "")

                writer.writerow([arrival_info, stop_number, stop_name, stop_id, lat, lng])

    print(f"✅ 資料已儲存為 {filename}")

# 主程式
if __name__ == "__main__":
    bus_route_id = input("請輸入公車代碼（例如 '0100000A00'）：")
    fetch_bus_data_to_csv(bus_route_id)
