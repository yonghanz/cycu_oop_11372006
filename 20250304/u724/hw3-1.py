import scipy.integrate as spi
import numpy as np

def f(x):
    return (x**2) * np.sqrt((x**3) + 1)

# 計算定積分從 0 到 3
result, error = spi.quad(f, 0, 3)
print(f"數值積分結果: {result}")

# 計算 x = 5 時的函數值
x_value = 5
y_value = f(x_value)
print(f"當 x = {x_value} 時, f(x) = {y_value}")

x_value = 30
y_value = f(x_value)
print(f"當 x = {x_value} 時, f(x) = {y_value}")

x_value = 100
y_value = f(x_value)
print(f"當 x = {x_value} 時, f(x) = {y_value}")

x_value = 1000
y_value = f(x_value)
print(f"當 x = {x_value} 時, f(x) = {y_value}")

x_value = 10000
y_value = f(x_value)
print(f"當 x = {x_value} 時, f(x) = {y_value}")