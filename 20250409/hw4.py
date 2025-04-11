import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

def run_sdof_response(direction, ax_displacement, ax_velocity, ax_acceleration):
    # === 1. 讀入地震資料 ===
    data = pd.read_csv("Northridge_NS.txt", sep="\s+", header=None, names=["Time", "Acceleration"])
    time = data["Time"].to_numpy()
    acc_g = data["Acceleration"].to_numpy()
    acc_in = acc_g * 386.4  # g -> in/s²

    # === 2. 設定參數 ===
    m = 0.7505  # kip·s²/in
    zeta = 0.05  # 阻尼比

    if direction == "NS":
        k = 368.136  # N-S 勁度 kips/in
    elif direction == "EW":
        k = 1209.667  # E-W 勁度 kips/in
    else:
        raise ValueError("方向請輸入 'NS' 或 'EW'")

    omega_n = np.sqrt(k / m)
    c = 2 * zeta * omega_n * m

    # === 3. 插值地震資料 ===
    ag_interp = interp1d(time, acc_in, fill_value="extrapolate")

    # === 4. 定義 SDOF 微分方程 ===
    def sdof_eq(t, y):
        u, v = y
        ag = ag_interp(t)
        a = (-c * v - k * u - m * ag) / m
        return [v, a]

    # === 5. 數值解 ===
    y0 = [0, 0]
    t_span = [time[0], time[-1]]
    sol = solve_ivp(sdof_eq, t_span, y0, t_eval=time)
    x = sol.y[0]
    v = sol.y[1]
    a = np.gradient(v, time)

    # === 6. 畫圖 ===
    ax_displacement.plot(time, x, label=f"{direction} Displacement")
    ax_velocity.plot(time, v, label=f"{direction} Velocity")
    ax_acceleration.plot(time, a, label=f"{direction} Acceleration")

    # === 7. 最大值列印 ===
    print(f"--- {direction} 方向最大反應值 ---")
    print("最大位移 (in):", np.max(np.abs(x)))
    print("最大速度 (in/s):", np.max(np.abs(v)))
    print("最大加速度 (in/s²):", np.max(np.abs(a)))


# === 同時跑 N-S 和 E-W ===
fig, (ax_displacement, ax_velocity, ax_acceleration) = plt.subplots(3, 1, figsize=(12, 12))

run_sdof_response("NS", ax_displacement, ax_velocity, ax_acceleration)
run_sdof_response("EW", ax_displacement, ax_velocity, ax_acceleration)

# 添加圖例和標籤
ax_displacement.set_title("Displacement History")
ax_displacement.set_xlabel("Time (s)")
ax_displacement.set_ylabel("Displacement (in)")
ax_displacement.legend()
ax_displacement.grid(True)

ax_velocity.set_title("Velocity History")
ax_velocity.set_xlabel("Time (s)")
ax_velocity.set_ylabel("Velocity (in/s)")
ax_velocity.legend()
ax_velocity.grid(True)

ax_acceleration.set_title("Acceleration History")
ax_acceleration.set_xlabel("Time (s)")
ax_acceleration.set_ylabel("Acceleration (in/s²)")
ax_acceleration.legend()
ax_acceleration.grid(True)

# 調整子圖之間的距離
plt.subplots_adjust(hspace=0.5)  # 調整子圖之間的垂直間距，值越大間距越大

plt.tight_layout()
plt.show()