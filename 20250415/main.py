
# %%

bus_code = input("請輸入id或是直接enter(默認0100026540)") or "0100026540"
url = "https://ebus.gov.taipei/Route/StopsOfRoute?routeid=" + bus_code
# url = "https://ebus.gov.taipei/Route/StopStatusOfRoute?routeid=" + bus_code
print(url)
fs = open("bus_stops.txt", "w", encoding="utf-8")
fs.write("公車到達時間,車站序號,車站名稱,車站編號,latitude,longitude\n")

# %%

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# 設定無頭模式（不開啟瀏覽器畫面）
options = Options()
options.add_argument("--headless")

# 開啟 Chrome 瀏覽器
driver = webdriver.Chrome(options=options)

# 開啟目標頁面
driver.get(url)

# 等待 JavaScript 執行
time.sleep(3)  # 可以改成 WebDriverWait 更穩定

# 抓下來的 HTML
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# 解析資料
print(soup.prettify())

driver.quit()


# %%
clo = False

for stop in soup.find_all("a"):
    # print(stop)
    # print(stop.get("class"))
    if stop.get("class") == ["auto-list-link", "auto-list-stationlist-link"]:
        print("----------------->")
        print(stop)
        print("<-----------------")
        for i in stop.find_all("span"):
            # <span class="auto-list auto-list-stationlist">
            # <span class="auto-list-stationlist-position auto-list-stationlist-position-none">今日未營運</span>
            # <span class="auto-list-stationlist-number"> 1</span>
            # <span class="auto-list-stationlist-place">萬芳社區</span>
            # <input id="item_UniStopId" name="item.UniStopId" type="hidden" value="1166500360"/>
            # <input data-val="true" data-val-number="欄位 Latitude 必須是數字。" data-val-required="Latitude 欄位是必要項。" id="item_Latitude" name="item.Latitude" type="hidden" value="25.001753"/>
            # <input data-val="true" data-val-number="欄位 Longitude 必須是數字。" data-val-required="Longitude 欄位是必要項。" id="item_Longitude" name="item.Longitude" type="hidden" value="121.570457"/>
            if i.get("class") == [
                "auto-list-stationlist-position",
                "auto-list-stationlist-position-none",
            ]:
                fs.write(i.text.strip() + ",")
                continue
            if i.get("class") == [
                "auto-list-stationlist-position",
                "auto-list-stationlist-position-now",
            ]:
                fs.write(i.text.strip() + ",")
                continue
            if i.get("class") == [
                "auto-list-stationlist-position",
                "auto-list-stationlist-position-time",
            ]:
                fs.write(i.text.strip() + ",")
                continue
            if i.get("class") == ["auto-list-stationlist-position"]:
                clo = True
                break
            if i.get("class") == ["auto-list-stationlist-number"]:
                fs.write(i.text.strip() + ",")
                continue
            if i.get("class") == ["auto-list-stationlist-place"]:
                fs.write(i.text.strip() + ",")
                continue
        if clo == True:
            break
        for i in stop.find_all("input"):
            # <input id="item_UniStopId" name="item.UniStopId" type="hidden" value="1166500360"/>
            # <input data-val="true" data-val-number="欄位 Latitude 必須是數字。" data-val-required="Latitude 欄位是必要項。" id="item_Latitude" name="item.Latitude" type="hidden" value="25.001753"/>
            # <input data-val="true" data-val-number="欄位 Longitude 必須是數字。" data-val-required="Longitude 欄位是必要項。" id="item_Longitude" name="item.Longitude" type="hidden" value="121.570457"/>
            if i.get("id") == "item_UniStopId":
                fs.write(i.get("value") + ",")
                continue
            if i.get("id") == "item_Latitude":
                fs.write(i.get("value") + ",")
                continue
            if i.get("id") == "item_Longitude":
                fs.write(i.get("value") + ",")
                continue
        fs.write("\n")

        if clo == True:
            break

# %%
fs.close()
print("完成，請查看bus_stops.txt")

# %%
