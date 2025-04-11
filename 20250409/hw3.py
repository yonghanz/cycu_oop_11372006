import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

# === 1. 讀入 Northridge 地震資料 ===
data = pd.read_csv("Northridge_NS.txt", sep="\s+", header=None, names=["Time", "Acceleration"])
time = data["Time"].to_numpy()
acc_g = data["Acceleration"].to_numpy()
acc_in = acc_g * 386.4  # 轉換為 in/s²

# === 2. 系統參數（E-W 方向） ===
m = 0.7505               # 質量 kip·s²/in
k = 1209.667             # 勁度 kips/in（E-W 抗風架剛度總和）
zeta = 0.05              # 阻尼比
omega_n = np.sqrt(k / m)        # 自然頻率
c = 2 * zeta * omega_n * m      # 阻尼係數

# === 3. 地震加速度插值函數 ===
ag_interp = interp1d(time, acc_in, fill_value="extrapolate")

# === 4. 定義微分方程（一階系統） ===
def sdof_eq(t, y):
    u, v = y
    ag = ag_interp(t)
    a = (-c * v - k * u - m * ag) / m
    return [v, a]

# === 5. 數值求解 ===
y0 = [0, 0]
t_span = [time[0], time[-1]]
sol = solve_ivp(sdof_eq, t_span, y0, t_eval=time)
x = sol.y[0]          # 位移
v = sol.y[1]          # 速度
a = np.gradient(v, time)  # 加速度

# === 6. 畫圖（黑白樣式） ===
plt.figure(figsize=(12, 4))
plt.plot(time, x, color="black", linestyle="-", label="Displacement")
plt.title("Displacement History (E-W)")
plt.xlabel("Time (s)")
plt.ylabel("Displacement (in)")
plt.grid(True, linestyle="--", color="gray", alpha=0.7)
plt.legend()
plt.show()

plt.figure(figsize=(12, 4))
plt.plot(time, v, color="black", linestyle="--", label="Velocity")
plt.title("Velocity History (E-W)")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (in/s)")
plt.grid(True, linestyle="--", color="gray", alpha=0.7)
plt.legend()
plt.show()

plt.figure(figsize=(12, 4))
plt.plot(time, a, color="black", linestyle="-.", label="Acceleration")
plt.title("Acceleration History (E-W)")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (in/s²)")
plt.grid(True, linestyle="--", color="gray", alpha=0.7)
plt.legend()
plt.show()

# === 7. 額外資訊 ===
print("最大位移 (in):", np.max(np.abs(x)))
print("最大速度 (in/s):", np.max(np.abs(v)))
print("最大加速度 (in/s²):", np.max(np.abs(a)))