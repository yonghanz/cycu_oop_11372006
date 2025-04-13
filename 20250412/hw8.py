import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 設定中文字體
rcParams['font.family'] = 'Heiti TC'

# 定義符號與常數
x, L, q, EI = sp.symbols('x L q EI')
pi = sp.pi
params = {L: 1, q: 1, EI: 1}

# 定義 w1, w2, w3
w1 = (-4 * pi * L**2 * q - 2 * L**2 * q + pi**3 * L**2 * q) * x **2  / (4 * pi**4 * EI)
w2 = (-2 * pi * L**2 * q - L**2 * q + pi**3 * L**2 * q)* x**2 / (2 * pi**4 * EI)  - (L * q * x**3) / (6 * pi * EI)
w3 = (-12 * pi**2 * L**2 * q - pi * L**2 * q + pi**4 * L**2 * q + 120 * L**2 * q)* x**2 / (2 * pi**5 * EI)  \
     + (-720 * L * q - pi**4 * L * q + 60 * pi**2 * L * q) * x**3 / (6 * pi**5 * EI) \
     + (-5 * pi**2 * q + 60 * q) * x**4 / (pi**5 * EI)

# 代入數值
w1 = w1.subs(params)
w2 = w2.subs(params)
w3 = w3.subs(params)

# 微分（一次微分）
dw1 = sp.diff(w1, x)
dw2 = sp.diff(w2, x)
dw3 = sp.diff(w3, x)

# 轉換為 numpy 函數
dw1_fn = sp.lambdify(x, -dw1, 'numpy')  # 轉角
dw2_fn = sp.lambdify(x, -dw2, 'numpy')
dw3_fn = sp.lambdify(x, -dw3, 'numpy')

# x 軸資料
x_vals = np.linspace(0, 1, 300)

# 計算數值
theta1 = dw1_fn(x_vals)
theta2 = dw2_fn(x_vals)
theta3 = dw3_fn(x_vals)

# 檢查數值範圍
print("theta1 範圍:", np.min(theta1), np.max(theta1))
print("theta2 範圍:", np.min(theta2), np.max(theta2))
print("theta3 範圍:", np.min(theta3), np.max(theta3))

# 畫圖
plt.figure(figsize=(10, 6))
plt.plot(x_vals, theta1, label=r'$-\frac{dw_1}{dx}$', color='blue')
plt.plot(x_vals, theta2, label=r'$-\frac{dw_2}{dx}$', color='green')
plt.plot(x_vals, theta3, label=r'$-\frac{dw_3}{dx}$', color='red')

# 添加標題和標籤
plt.title("轉角圖（一次微分）", fontsize=16)
plt.xlabel("x", fontsize=14)
plt.ylabel("轉角", fontsize=14)
plt.legend()
plt.grid(True)

# 顯示圖形
plt.show()
