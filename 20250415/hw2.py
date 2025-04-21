from datetime import datetime

def analyze_date(input_time):
    """
    分析輸入的時間字串，完成以下任務：
    1. 回傳該日期為星期幾。
    2. 回傳該日期是當年的第幾天。
    3. 計算從該時刻至現在時間，共經過了幾個太陽日（Julian date）。

    參數:
    - input_time: 時間字串，格式為 "YYYY-MM-DD HH:MM"。

    回傳:
    - 星期幾（例如: 星期三）
    - 當年的第幾天（day of year）
    - 經過的太陽日（以浮點數表示）
    """
    # 將輸入的時間字串轉換為 datetime 物件
    input_datetime = datetime.strptime(input_time, "%Y-%m-%d %H:%M")

    # 1. 計算星期幾
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[input_datetime.isoweekday() - 1]

    # 2. 計算當年的第幾天
    day_of_year = input_datetime.timetuple().tm_yday

    # 3. 計算從該時刻至現在時間的太陽日（以 Julian 日期計算差值）
    now = datetime.now()

    # Julian 日期的簡化計算：以距離 now 的天數（秒除以 86400）
    julian_days = (now - input_datetime).total_seconds() / 86400

    return weekday, day_of_year, julian_days


# 主程式：使用者輸入時間
if __name__ == "__main__":
    try:
        input_time = input("請輸入時間字串 (格式: YYYY-MM-DD HH:MM): ")
        weekday, day_of_year, julian_days = analyze_date(input_time)
        print(f"輸入的日期為: {weekday}")
        print(f"該日期是當年的第 {day_of_year} 天")
        print(f"從該時刻至現在，共經過了 {julian_days:.2f} 個太陽日")
    except ValueError:
        print("請輸入正確的時間格式！格式應為 YYYY-MM-DD HH:MM")
