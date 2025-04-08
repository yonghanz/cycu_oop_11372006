import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

def plot_lognormal_cdf(mu, sigma):
    """
    繪製對數常態累積分布函數 (Log-normal CDF)
    
    :param mu: 對數常態分布的 μ
    :param sigma: 對數常態分布的 σ
    """
    # 計算對數常態分布的形狀參數
    shape = sigma
    scale = np.exp(mu)

    # 定義 x 範圍
    x = np.linspace(0.01, 10, 500)

    # 計算累積分布函數 (CDF)
    cdf = lognorm.cdf(x, shape, scale=scale)

    # 繪製圖表
    plt.figure(figsize=(8, 6))
    plt.plot(x, cdf, label=f'Log-normal CDF (μ={mu}, σ={sigma})', color='blue')
    plt.title('Log-normal Cumulative Distribution Function')
    plt.xlabel('x')
    plt.ylabel('CDF')
    plt.legend()
    plt.grid()

    # 儲存圖表為 JPG 檔案
    filename = f'lognormal_cdf_mu{mu}_sigma{sigma}.jpg'
    plt.savefig(filename, format='jpg')
    plt.show()
    print(f"圖表已儲存為 {filename}")

# 主程式
if __name__ == "__main__":
    try:
        # 提示用戶輸入 μ 和 σ
        mu = float(input("請輸入 μ 的值："))
        sigma = float(input("請輸入 σ 的值："))
        plot_lognormal_cdf(mu, sigma)
    except ValueError:
        print("輸入的值必須是數字！")