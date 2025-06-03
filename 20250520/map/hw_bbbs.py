import os  # 確保匯入 os 模組
import geopandas as gpd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
from matplotlib import rcParams

# 設置支持中文的字型
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 從使用者輸入獲取公車代碼
route_id = input("請輸入公車代碼（例如 0161000900）: ").strip()

# 找出 taipei_town 目錄下的第一個 .shp 檔案
shp_dir = "20250520/map"
shp_file = None
for fname in os.listdir(shp_dir):
    if fname.endswith(".shp"):
        shp_file = os.path.join(shp_dir, fname)
        break

if shp_file is None:
    print("No shapefile found in", shp_dir)
else:
    # 讀取 shapefile
    gdf = gpd.read_file(shp_file)
    
    # 篩選出桃園市、臺北市、新北市和基隆市的資料，假設屬性欄位名稱為 "COUNTYNAME"
    target_cities = ["桃園市", "臺北市", "新北市", "基隆市"]
    filtered_gdf = gdf[gdf["COUNTYNAME"].isin(target_cities)]
    
    # 從 SQLite 資料庫中讀取指定公車代碼的站點座標
    db_file = "data/hermes_ebus_taipei.sqlite3"
    engine = create_engine(f"sqlite:///{db_file}")
    query = f"""
        SELECT stop_name, latitude, longitude
        FROM data_route_info_busstop
        WHERE route_id = '{route_id}'
    """
    bus_stops = pd.read_sql(query, engine)

    if bus_stops.empty:
        print(f"未找到公車代碼 {route_id} 的站點資料。")
    else:
        # 將站點資料轉換為 GeoDataFrame
        bus_stops_gdf = gpd.GeoDataFrame(
            bus_stops,
            geometry=gpd.points_from_xy(bus_stops["longitude"], bus_stops["latitude"]),
            crs="EPSG:4326"
        )

        # 繪製地圖
        fig, ax = plt.subplots(figsize=(10, 10))
        filtered_gdf.plot(ax=ax, edgecolor='black', color='lightgray', alpha=0.5)
        bus_stops_gdf.plot(ax=ax, color='red', markersize=50, label='Bus Stops')

        plt.title(f"Bus Stops for Route {route_id} on Selected Cities Map")
        plt.axis('equal')
        plt.legend()

        # 儲存地圖為圖片
        output_file = f"bus_stops_route_{route_id}.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"地圖已儲存為 {output_file}")

        plt.show()