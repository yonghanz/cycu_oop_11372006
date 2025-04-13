import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 設定支援中文字體
rcParams['font.family'] = 'Heiti TC'

# 定義符號
x, L, q, EI = sp.symbols('x L q EI')
pi = sp.pi

# 定義 w1(x), w2(x), w3(x)
w1 = (-4*pi*L**2*q - 2*L**2*q + pi**3*L**2*q) * x**2 / (4*pi**4*EI)
w2 = (-2*pi*L**2*q - L**2*q + pi**3*L**2*q) * x**2 / (2*pi**4*EI) - (L*q*x**3) / (6*pi*EI)
w3 = (-12*pi**2*L**2*q - pi*L**2*q + pi**4*L**2*q + 120*L**2*q) * x**2 / (2*pi**5*EI) \
    + (-720*L*q - pi**4*L*q + 60*pi**2*L*q) * x**3 / (6*pi**5*EI) \
    + (-5*pi**2*q + 60*q) * x**4 / (pi**5*EI)

# 替換參數
params = {EI: 1, q: 1, L: 1}
w1_func = w1.subs(params).doit().evalf()
w2_func = w2.subs(params).doit().evalf()
w3_func = w3.subs(params).doit().evalf()

# 微分一次（轉角）
dw1_dx = -sp.diff(w1_func, x).doit()
dw2_dx = -sp.diff(w2_func, x).doit()
dw3_dx = -sp.diff(w3_func, x).doit()

# 微分二次（曲率 / 彎矩）
d2w1_dx2 = sp.diff(w1_func, x, 2).doit()
d2w2_dx2 = sp.diff(w2_func, x, 2).doit()
d2w3_dx2 = sp.diff(w3_func, x, 2).doit()

# 轉換為 numpy 函數
dw1_fn = sp.lambdify(x, dw1_dx, 'numpy')
dw2_fn = sp.lambdify(x, dw2_dx, 'numpy')
dw3_fn = sp.lambdify(x, dw3_dx, 'numpy')

M1_fn = sp.lambdify(x, d2w1_dx2, 'numpy')
M2_fn = sp.lambdify(x, d2w2_dx2, 'numpy')
M3_fn = sp.lambdify(x, d2w3_dx2, 'numpy')

# x 軸
x_vals = np.linspace(0, 1, 200)

# 轉角
theta1_vals = dw1_fn(x_vals)
theta2_vals = dw2_fn(x_vals)
theta3_vals = dw3_fn(x_vals)

# 彎矩
M1_vals = M1_fn(x_vals)
M2_vals = M2_fn(x_vals)
M3_vals = M3_fn(x_vals)

# 畫圖
fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# 轉角圖
axs[0].plot(x_vals, theta1_vals, label=r'$-\frac{dw_1}{dx}$', color='blue')
axs[0].plot(x_vals, theta2_vals, label=r'$-\frac{dw_2}{dx}$', color='green')
axs[0].plot(x_vals, theta3_vals, label=r'$-\frac{dw_3}{dx}$', color='red')
axs[0].set_title("梁轉角圖（一次微分）", fontsize=16)
axs[0].set_ylabel("轉角", fontsize=14)
axs[0].legend()
axs[0].grid(True)

# 彎矩圖（二次微分）
axs[1].plot(x_vals, M1_vals, label=r'$\frac{d^2w_1}{dx^2}$', color='blue')
axs[1].plot(x_vals, M2_vals, label=r'$\frac{d^2w_2}{dx^2}$', color='green')
axs[1].plot(x_vals, M3_vals, label=r'$\frac{d^2w_3}{dx^2}$', color='red')
axs[1].set_title("梁彎矩圖（二次微分）", fontsize=16)
axs[1].set_xlabel("x", fontsize=14)
axs[1].set_ylabel("彎矩", fontsize=14)
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()
