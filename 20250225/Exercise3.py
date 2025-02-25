def print_right(text):
    # 計算需要的前置空格數量
    leading_spaces = 40 - len(text)
    # 使用字串重複運算符 (*) 來生成前置空格，並將其與原始字串連接
    result = ' ' * leading_spaces + text
    # 打印結果
    print(result)

# 測試範例
print_right("Monty")
print_right("Python's")
print_right("Flying Circus")