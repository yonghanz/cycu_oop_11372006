def find_non_multiples():
    non_multiples = []
    for number in range(1, 101):
        if number % 2 != 0 and number % 3 != 0 and number % 5 != 0 and number % 7 != 0:
            non_multiples.append(number)
    return non_multiples

# 列出 1 到 100 中不是 2, 3, 5, 7 倍數的數字
result = find_non_multiples()
print("1 到 100 中不是 2, 3, 5, 7 倍數的數字有:", result)