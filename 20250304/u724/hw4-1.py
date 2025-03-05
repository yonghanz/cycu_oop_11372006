def find_first_even(numbers):
    for number in numbers:
        if number % 2 == 0:
            print(f"找到第一個偶數: {number}")
            break
    else:
        print("列表中沒有偶數")

# 測試範例
numbers = [1, 3, 5, 7, 8, 9]
find_first_even(numbers)

numbers = [1, 3, 5, 7, 9]
find_first_even(numbers)