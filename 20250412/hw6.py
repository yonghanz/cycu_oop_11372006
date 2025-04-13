import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 設置 Heiti TC 字體為支持中文的字體
rcParams['font.family'] = 'Heiti TC'  # 設置字體為 Heiti TC

# 定義符號
x, L, q, EI = sp.symbols('x L q EI')
pi = sp.pi

# 定義 w1(x), w2(x), w3(x)
w1 = (-4 * pi * L**2 * q - 2 * L**2 * q + pi**3 * L**2 * q) * x **2  / (4 * pi**4 * EI)
w2 = (-2 * pi * L**2 * q - L**2 * q + pi**3 * L**2 * q)* x**2 / (2 * pi**4 * EI)  - (L * q * x**3) / (6 * pi * EI)
w3 = (-12 * pi**2 * L**2 * q - pi * L**2 * q + pi**4 * L**2 * q + 120 * L**2 * q)* x**2 / (2 * pi**5 * EI)  \
     + (-720 * L * q - pi**4 * L * q + 60 * pi**2 * L * q) * x**3 / (6 * pi**5 * EI) \
     + (-5 * pi**2 * q + 60 * q) * x**4 / (pi**5 * EI)

# 假設 EI=1, q=1, L=1
EI_value = 1
q_value = 1
L_value = 1

# 替換參數值
w1_func = w1.subs({EI: EI_value, q: q_value, L: L_value})
w2_func = w2.subs({EI: EI_value, q: q_value, L: L_value})
w3_func = w3.subs({EI: EI_value, q: q_value, L: L_value})

# 對 w1, w2, w3 求導
dw1_dx = sp.diff(w1_func, x)
dw2_dx = sp.diff(w2_func, x)
dw3_dx = sp.diff(w3_func, x)

# 將 SymPy 表達式轉換為可計算的函數
dw1_dx_lambdified = sp.lambdify(x, -dw1_dx, 'numpy')  # 取負值
dw2_dx_lambdified = sp.lambdify(x, -dw2_dx, 'numpy')  # 取負值
dw3_dx_lambdified = sp.lambdify(x, -dw3_dx, 'numpy')  # 取負值

# 定義 x 軸數據
x_values = np.linspace(0, L_value, 100)

# 計算 -dw1(x)/dx, -dw2(x)/dx, -dw3(x)/dx 的值
dw1_dx_values = dw1_dx_lambdified(x_values)
dw2_dx_values = dw2_dx_lambdified(x_values)
dw3_dx_values = dw3_dx_lambdified(x_values)

# 繪製圖形
plt.figure(figsize=(10, 6))
plt.plot(x_values, dw1_dx_values, label=r'$-\frac{dw_1(x)}{dx}$', color='blue')
plt.plot(x_values, dw2_dx_values, label=r'$-\frac{dw_2(x)}{dx}$', color='green')
plt.plot(x_values, dw3_dx_values, label=r'$-\frac{dw_3(x)}{dx}$', color='red')

# 添加標籤和圖例
plt.title("(EI=1, q=1, L=1) -dw(x)/dx 轉角", fontsize=16)
plt.xlabel("x", fontsize=14)
plt.ylabel(r"$-\frac{dw(x)}{dx}$", fontsize=14)
plt.legend()
plt.grid(True)

# 顯示圖形
plt.show()