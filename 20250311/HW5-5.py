from lunarcalendar.converter import Converter, Solar

# create a list fill with weekdays from Monday to Sunday
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# create a list fill with Month from January to December
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# 一個可以放十二生肖的 list mouse, ox, tiger, rabbit, dragon, snake, horse, sheep, monkey, rooster, dog, pig
zodiac = ['mouse', 'ox', 'tiger', 'rabbit', 'dragon', 'snake', 'horse', 'sheep', 'monkey', 'rooster', 'dog', 'pig']

def get_zodiac(year):
    # 以 1900 年為基準，1900 年是鼠年
    base_year = 1900
    index = (year - base_year) % 12
    return zodiac[index]

def convert_to_lunar(year, month, day):
    solar_date = Solar(year, month, day)
    lunar_date = Converter.Solar2Lunar(solar_date)
    return lunar_date

# get user input for the year, month, and day
year = int(input('Enter the year: '))
month = int(input('Enter the month: '))
day = int(input('Enter the day: '))

# convert to lunar date
lunar_date = convert_to_lunar(year, month, day)
print(f'The lunar date is {lunar_date}')

# print the zodiac sign for the given year
print(f'The year {lunar_date.year} is the year of the {get_zodiac(lunar_date.year)}.')