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

# 將 SymPy 表達式轉換為可計算的函數
w1_lambdified = sp.lambdify(x, w1_func, 'numpy')
w2_lambdified = sp.lambdify(x, w2_func, 'numpy')
w3_lambdified = sp.lambdify(x, w3_func, 'numpy')

# 定義 x 軸數據
x_values = np.linspace(0, L_value, 100)

# 計算 -w1(x), -w2(x), -w3(x) 的值
w1_values = -w1_lambdified(x_values)
w2_values = -w2_lambdified(x_values)
w3_values = -w3_lambdified(x_values)

# 繪製圖形
plt.figure(figsize=(10, 6))
plt.plot(x_values, w1_values, label=r'$-w_1(x)$', color='blue')
plt.plot(x_values, w2_values, label=r'$-w_2(x)$', color='green')
plt.plot(x_values, w3_values, label=r'$-w_3(x)$', color='red')

# 添加標籤和圖例
plt.title("(EI=1, q=1, L=1) 位移", fontsize=16)
plt.xlabel("x", fontsize=14)
plt.ylabel("-w(x)", fontsize=14)
plt.legend()
plt.grid(True)

# 顯示圖形
plt.show()