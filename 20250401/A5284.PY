import requests
import html
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate

url = '''https://pda5284.gov.taipei/MQS/route.jsp?rid=10417'''

try:
    # 發送 GET 請求
    response = requests.get(url)
    response.raise_for_status()  # 檢查 HTTP 狀態碼
except requests.exceptions.RequestException as e:
    print(f"請求失敗：{e}")
    exit()

try:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到所有表格
    tables = soup.find_all("table")

    # 初始化去程和回程的資料列表
    outbound_rows = []
    return_rows = []

    # 遍歷表格
    for table in tables:
        # 去程資料
        for tr in table.find_all("tr", class_=["ttego1", "ttego2"]):
            td = tr.find("td")
            if td:
                stop_name = html.unescape(td.text.strip())  # 解碼站點名稱
                stop_link = td.find("a")["href"] if td.find("a") else None
                if stop_link:  # 只保留有連結的站點
                    outbound_rows.append({"站點名稱": stop_name, "連結": stop_link})

        # 回程資料
        for tr in table.find_all("tr", class_=["tteback1", "tteback2"]):
            td = tr.find("td")
            if td:
                stop_name = html.unescape(td.text.strip())  # 解碼站點名稱
                stop_link = td.find("a")["href"] if td.find("a") else None
                if stop_link:  # 只保留有連結的站點
                    return_rows.append({"站點名稱": stop_name, "連結": stop_link})

    # 轉換去程和回程資料為 DataFrame
    if outbound_rows:
        outbound_df = pd.DataFrame(outbound_rows)
        print("去程站點資料：")
        print(tabulate(outbound_df, headers="keys", tablefmt="grid", showindex=False))
        # 保存去程資料為 CSV
        outbound_df.to_csv("去程站點資料.csv", index=False, encoding="utf-8-sig")
        print("去程資料已保存為 '去程站點資料.csv'")

    if return_rows:
        return_df = pd.DataFrame(return_rows)
        print("\n回程站點資料：")
        print(tabulate(return_df, headers="keys", tablefmt="grid", showindex=False))
        # 保存回程資料為 CSV
        return_df.to_csv("回程站點資料.csv", index=False, encoding="utf-8-sig")
        print("回程資料已保存為 '回程站點資料.csv'")

    if not outbound_rows and not return_rows:
        print("未找到足夠的表格資料。")
except Exception as e:
    print(f"資料處理失敗：{e}")
    exit()