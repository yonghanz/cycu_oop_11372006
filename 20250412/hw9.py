import numpy as np
import matplotlib.pyplot as plt

# 基本參數
L = 1
q0 = 1
EI = 1
pi = np.pi

# x 軸
x = np.linspace(0, L, 500)

# === N = 1 ===
a1_n1 = (q0 * L**2 / (2 * EI)) * (1 / pi**3 + 1 / pi**2)
w_n1 = -a1_n1 * x**2
theta_n1 = -2 * a1_n1 * x
moment_n1 = -(-EI * (2 * a1_n1) * np.ones_like(x))
shear_n1 = np.zeros_like(x)

# === N = 2 ===
a1_n2 = q0 / EI * (L**2 / (2*pi) - L / pi**3 + 2*L / pi**4)
a2_n2 = q0 / EI * (-L / (6*pi) + 3 / (2*pi**4))
w_n2 = -(a1_n2 * x**2 + a2_n2 * x**3)
theta_n2 = -(2 * a1_n2 * x + 3 * a2_n2 * x**2)
moment_n2 = -(-EI * (2 * a1_n2 + 6 * a2_n2 * x))
shear_n2 = -(-EI * (6 * a2_n2 * np.ones_like(x)))

# === N = 3 ===
a1_n3 = L**2 * q0 * (pi**3 + 9*pi**2 - 36*pi + 60) / (2 * EI * pi**5)
a2_n3 = 2 * L * q0 * (-3*pi**2 + 16*pi - 30) / (EI * pi**5)
a3_n3 = 5 * q0 * (pi**2 - 6*pi + 12) / (2 * EI * pi**5)
w_n3 = -(a1_n3 * x**2 + a2_n3 * x**3 + a3_n3 * x**4)
theta_n3 = -(2 * a1_n3 * x + 3 * a2_n3 * x**2 + 4 * a3_n3 * x**3)
moment_n3 = (-EI * (2 * a1_n3 + 6 * a2_n3 * x + 12 * a3_n3 * x**2))
shear_n3 = -(-EI * (6 * a2_n3 + 24 * a3_n3 * x))

# === 正確解 ===
w_exact = (q0 * L**4 / (EI * pi**4)) * (np.sin(pi * x / L) - pi * x / L)
theta_exact = (q0 * L**3 / (EI * pi**3)) * (np.cos(pi * x / L) - 1)
moment_exact = (q0 * L**2 / pi**2) * np.sin(pi * x / L)
shear_exact = (q0 * L) * np.cos(pi * x / L)

# === 繪圖 ===
def plot_with_exact(title, y1, y2, y3, y_exact, ylabel):
    plt.figure()
    plt.plot(x, y1, label='N=1')
    plt.plot(x, y2, label='N=2')
    plt.plot(x, y3, label='N=3')
    plt.plot(x, y_exact, label='Exact', linestyle='--')
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()

plot_with_exact('Displacement w(x) (negative)', w_n1, w_n2, w_n3, w_exact, 'w(x)')
plot_with_exact('Rotation θ(x) = dw/dx (negative)', theta_n1, theta_n2, theta_n3, theta_exact, 'θ(x)')
plot_with_exact('Moment M(x) = -EI d²w/dx² (negative)', moment_n1, moment_n2, moment_n3, moment_exact, 'M(x)')
plot_with_exact('Shear Force V(x) = -EI d³w/dx³ (negative)', shear_n1, shear_n2, shear_n3, shear_exact, 'V(x)')

plt.show()