import matplotlib.pyplot as plt
import numpy as np

# 生成 x 軸數據
x = np.linspace(0, 10, 100)

# 定義三條曲線的 y 軸數據
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)

# 繪製三條曲線
plt.plot(x, y1, 'r-', label='sin(x)')  # 紅色實線
plt.plot(x, y2, 'g--', label='cos(x)')  # 綠色虛線
plt.plot(x, y3, 'b-.', label='tan(x)')  # 藍色點劃線

# 添加標籤和標題
plt.xlabel('x')
plt.ylabel('y')
plt.title('Curve graphics') # 圖形標題

# 顯示圖例
plt.legend()

# 顯示圖形
plt.show()