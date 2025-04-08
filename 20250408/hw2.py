from datetime import datetime

def calculate_julian_date(input_time_str):
    """
    計算輸入時間的星期幾以及距今的太陽日數（Julian date）。
    
    :param input_time_str: 輸入時間，格式為 "YYYY-MM-DD HH:SS"
    :return: 該天是星期幾，以及距今的太陽日數
    """
    # 定義 Julian 日期的起始點
    julian_start = datetime(4713, 1, 1, 12)  # 公元前 4713 年 1 月 1 日 12:00

    # 將輸入的時間字串轉換為 datetime 物件
    input_time = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")

    # 計算該天是星期幾
    weekday = input_time.strftime("%A")  # 星期幾（英文）

    # 計算輸入時間的 Julian 日期
    julian_date_input = (input_time - julian_start).total_seconds() / 86400

    # 計算當前時間的 Julian 日期
    now = datetime.now()
    julian_date_now = (now - julian_start).total_seconds() / 86400

    # 計算距今的太陽日數
    days_elapsed = julian_date_now - julian_date_input

    return weekday, days_elapsed

# 測試函數
if __name__ == "__main__":
    input_time_str = input("請輸入時間 (格式為 YYYY-MM-DD HH:SS)：")  # 提示用戶輸入時間
    try:
        weekday, days_elapsed = calculate_julian_date(input_time_str)
        print(f"輸入的時間是星期：{weekday}")
        print(f"距今的太陽日數為：{days_elapsed:.6f}")
    except ValueError:
        print("輸入格式錯誤！請使用格式 YYYY-MM-DD HH:SS")