def product_of_odds(n):
    product = 1
    for i in range(1, n + 1, 2):  # 只取奇數 (步長為2)
        product *= i
    return product

def product_of_odds_last_digit(n):
    product = product_of_odds(n)
    return product % 10

# 測試範例
n = int(input("請輸入一個正整數 N: "))
print(f"1 到 {n} 之間所有奇數的乘積為: {product_of_odds(n)}")


from functools import reduce

def multiply_odd_numbers(numbers):
    odd_numbers = [num for num in numbers if num % 2 == 1]  # 過濾奇數
    return reduce(lambda x, y: x * y, odd_numbers, 1)  # 使用 reduce 計算乘積

# 測試範例
numbers = [3, 7, 2, 5, 8, 9]
print(f"列表中所有奇數的乘積為: {multiply_odd_numbers(numbers)}")
N:11