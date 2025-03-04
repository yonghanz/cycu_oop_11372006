def sum_of_powers(x, m):
    total = 0
    for i in range(m + 1):
        total += x ** i
    return total


x = 0.99
m = 3
print(f"從 {x} 的 0 次方加到 {x} 的 {m} 次方的總和:", sum_of_powers(x, m))

x = 0.99
m = 10
print(f"從 {x} 的 0 次方加到 {x} 的 {m} 次方的總和:", sum_of_powers(x, m))

x = 0.99
m = 50
print(f"從 {x} 的 0 次方加到 {x} 的 {m} 次方的總和:", sum_of_powers(x, m))

x = 0.99
m = 200
print(f"從 {x} 的 0 次方加到 {x} 的 {m} 次方的總和:", sum_of_powers(x, m))

x = 0.99
m = 400
print(f"從 {x} 的 0 次方加到 {x} 的 {m} 次方的總和:", sum_of_powers(x, m))

x = 0.99
m = int(1/(1-x))  # 將 m 轉換為整數
print(f"從 {x} 的 0 次方加到 {x} 的 {m} 次方的總和:", sum_of_powers(x, m))