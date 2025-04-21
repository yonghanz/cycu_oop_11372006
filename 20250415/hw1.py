import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib import rcParams

# 設定支援中文的字體
rcParams['font.family'] = 'Heiti TC'  # 替換為系統中支持的中文字體名稱

def plot_normal_pdf(mu, sigma, filename="normal_pdf.jpg"):
    """
    繪製常態分布的機率密度函數 (PDF) 並儲存為 JPG 圖檔。

    參數:
    - mu: 常態分布的平均值
    - sigma: 常態分布的標準差
    - filename: 儲存的圖檔名稱 (預設為 "normal_pdf.jpg")
    """
    # 定義 x 軸範圍
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 500)
    
    # 計算 PDF 值
    pdf = norm.pdf(x, mu, sigma)
    
    # 繪製圖形
    plt.figure(figsize=(8, 5))
    plt.plot(x, pdf, label=f"$\mu={mu}, \sigma={sigma}$", color="blue")
    plt.title("常態分布機率密度函數 (PDF)", fontsize=16)
    plt.xlabel("x", fontsize=14)
    plt.ylabel("PDF", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True)
    
    # 儲存圖檔
    plt.savefig(filename, format="jpg")
    plt.close()
    print(f"圖形已儲存為 {filename}")

# 動態輸入 mu 和 sigma
try:
    mu = float(input("請輸入常態分布的平均值 mu: "))
    sigma = float(input("請輸入常態分布的標準差 sigma: "))
    
    
    # 呼叫函數繪製圖形
    plot_normal_pdf(mu, sigma)
except ValueError:
    print("請輸入有效的數值！")