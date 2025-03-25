import requests
from bs4 import BeautifulSoup

def fetch_bus_routes(url):
    """
    從指定網址抓取所有公車路線清單
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 假設公車路線的連結在 <a> 標籤中，並有特定 class
        routes = soup.find_all('a', class_='route-link')  # 根據實際 HTML 結構調整
        route_list = {route.text.strip(): route['href'] for route in routes}

        print("找到的公車路線：")
        for route_name in route_list.keys():
            print(route_name)

        return route_list
    except Exception as e:
        print(f"抓取公車路線時發生錯誤: {e}")
        return {}

def fetch_bus_arrival_time(route_url, bus_stop):
    """
    查詢特定公車路線的到站時間
    """
    try:
        response = requests.get(route_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 假設到站時間在特定的 HTML 標籤中
        stops = soup.find_all('div', class_='stop-name')  # 根據實際 HTML 結構調整
        times = soup.find_all('div', class_='arrival-time')  # 根據實際 HTML 結構調整

        stop_time_map = {stop.text.strip(): time.text.strip() for stop, time in zip(stops, times)}

        if bus_stop in stop_time_map:
            print(f"{bus_stop} 的到站時間是：{stop_time_map[bus_stop]}")
        else:
            print(f"找不到公車站牌：{bus_stop}")

        return stop_time_map
    except Exception as e:
        print(f"查詢到站時間時發生錯誤: {e}")
        return {}

if __name__ == "__main__":
    # 公車路線清單網址
    route_list_url = "https://pda5284.gov.taipei/MQS/routelist.jsp"

    # 抓取所有公車路線
    routes = fetch_bus_routes(route_list_url)

    # 使用者輸入公車路線名稱
    bus_route = input("請輸入公車路線名稱：")
    if bus_route in routes:
        route_url = routes[bus_route]

        # 使用者輸入公車站牌名稱
        bus_stop = input("請輸入公車站牌名稱：")
        fetch_bus_arrival_time(route_url, bus_stop)
    else:
        print("找不到該公車路線！")