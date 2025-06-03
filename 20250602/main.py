# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# 使用者輸入公車路線代碼
bus_code = input("請輸入id或是直接enter(默認0100026540): ") or "0100026540"
url = "https://ebus.gov.taipei/Route/StopsOfRoute?routeid=" + bus_code
print(url)

# 設定無頭模式（不開啟瀏覽器畫面）
options = Options()
options.add_argument("--headless")  # 無頭模式
options.add_argument("--disable-gpu")  # 禁用 GPU 渲染
options.add_argument("--no-sandbox")  # 避免沙盒問題
options.add_argument("--disable-dev-shm-usage")  # 避免資源不足問題

# 使用 webdriver_manager 自動下載和管理 ChromeDriver
service = Service(ChromeDriverManager().install())

# 開啟 Chrome 瀏覽器
driver = webdriver.Chrome(service=service, options=options)

try:
    # 開啟目標頁面
    driver.get(url)

    # 等待 JavaScript 執行
    time.sleep(3)  # 可以改成 WebDriverWait 更穩定

    # 抓下來的 HTML
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 解析資料
    print(soup.prettify())

finally:
    driver.quit()
