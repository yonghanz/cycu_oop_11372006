from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# 使用者輸入公車路線代碼
bus_code = input("請輸入id或是直接enter(默認0100026540): ") or "0100026540"
url = "https://ebus.gov.taipei/Route/StopsOfRoute?routeid=" + bus_code
print(url)

# 設定無頭模式（不開啟瀏覽器畫面）
options = Options()
options.add_argument("--headless")

# 開啟 Chrome 瀏覽器
driver = webdriver.Chrome(options=options)

try:
    # 開啟目標頁面
    driver.get(url)

    # 等待頁面加載完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "auto-list-link"))
    )

    # 抓下來的 HTML
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 儲存資料到檔案
    with open("bus_stops.txt", "w", encoding="utf-8") as fs:
        fs.write("公車到達時間,車站序號,車站名稱,車站編號,latitude,longitude\n")
        for stop in soup.find_all("a", class_="auto-list-link auto-list-stationlist-link"):
            for span in stop.find_all("span"):
                span_class = span.get("class", [])
                if "auto-list-stationlist-position" in span_class:
                    fs.write(span.text.strip() + ",")
                elif "auto-list-stationlist-number" in span_class:
                    fs.write(span.text.strip() + ",")
                elif "auto-list-stationlist-place" in span_class:
                    fs.write(span.text.strip() + ",")
            for input_tag in stop.find_all("input"):
                input_id = input_tag.get("id", "")
                if input_id in ["item_UniStopId", "item_Latitude", "item_Longitude"]:
                    fs.write(input_tag.get("value", "") + ",")
            fs.write("\n")

    print("完成，請查看 bus_stops.txt")

except Exception as e:
    print(f"發生錯誤：{e}")

finally:
    driver.quit()
