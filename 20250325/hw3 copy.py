import requests
import datetime
import hashlib
import hmac
import base64

# PTX API 的基本設定
PTX_BASE_URL = "https://pda5284.gov.taipei/MQS/stoplocation.jsp?slid=3122"
APP_ID = "你的AppID"  # 替換為您的 App ID
APP_KEY = "你的AppKey"  # 替換為您的 App Key

def get_auth_header():
    """
    生成 PTX API 所需的簽章驗證標頭
    """
    # 使用時區感知的 UTC 時間
    x_date = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    hashed = hmac.new(
        APP_KEY.encode('utf-8'),  # 確保使用 UTF-8 編碼
        ("x-date: " + x_date).encode('utf-8'),
        hashlib.sha1
    ).digest()
    signature = base64.b64encode(hashed).decode('utf-8')  # 確保使用 UTF-8 解碼
    authorization = f'hmac username="{APP_ID}", algorithm="hmac-sha1", headers="x-date", signature="{signature}"'
    return {
        "Authorization": authorization,
        "x-date": x_date,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

def fetch_bus_dynamic_info(route_name, stop_name):
    """
    查詢指定公車路線和站牌的動態到站資訊
    """
    try:
        # 發送 GET 請求
        url = f"{PTX_BASE_URL}/{route_name}?$format=JSON"
        headers = get_auth_header()
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 解析回應的 JSON 資料
        data = response.json()

        # 過濾出指定站牌的到站資訊
        for item in data:
            if item.get("StopName", {}).get("Zh_tw") == stop_name:
                estimate_time = item.get("EstimateTime")
                if estimate_time is not None:
                    minutes = estimate_time // 60
                    print(f"公車 {route_name} 即將在 {stop_name} 到站，預估時間：{minutes} 分鐘")
                else:
                    print(f"公車 {route_name} 尚未發車或無到站資訊")
                return

        print(f"找不到公車 {route_name} 在站牌 {stop_name} 的到站資訊")
    except Exception as e:
        print(f"查詢公車動態資訊時發生錯誤: {e}")

if __name__ == "__main__":
    # 使用者輸入公車路線名稱
    bus_route = input("請輸入公車路線名稱：")
    # 使用者輸入公車站牌名稱
    bus_stop = input("請輸入公車站牌名稱：")

    # 查詢公車動態資訊
    fetch_bus_dynamic_info(bus_route, bus_stop)
