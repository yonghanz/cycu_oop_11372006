import requests
from bs4 import BeautifulSoup

def get_bus_arrival_time(station_name: str):
    # 公車動態資料的 API 或網頁 URL
    url = "https://pda5284.gov.taipei/MQS/RouteDyna?routeid=10417"

    # 發送 GET 請求
    response = requests.get(url)
    if response.status_code != 200:
        print("無法取得公車資料，請稍後再試。")
        return

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到所有站點資料
    rows = soup.find_all("tr", class_=["ttego1", "ttego2", "tteback1", "tteback2"])

    # 初始化結果
    found = False

    # 遍歷每一列，查找對應的站名
    for row in rows:
        try:
            stop_name = row.find_all("td")[1].text.strip()  # 提取站名
            arrival_time = row.find_all("td")[3].text.strip()  # 提取到站時間

            if station_name in stop_name:  # 部分匹配站名
                print(f"站名: {stop_name}, 預估到站時間: {arrival_time}")
                found = True
        except IndexError:
            continue

    if not found:
        print("查無此站，請確認輸入的站名是否正確。")

# 主程式
if __name__ == "__main__":
    station_name = input("請輸入站名: ")
    get_bus_arrival_time(station_name)
    