import os
import geopandas as gpd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
from matplotlib import rcParams

# 設置支持中文的字型
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 從 SQLite 資料庫中讀取站點和路線資料
db_file = "data/hermes_ebus_taipei.sqlite3"
engine = create_engine(f"sqlite:///{db_file}")

# 查詢所有站點資料
query_stops = """
    SELECT stop_name, route_id 
    FROM data_route_info_busstop
"""
bus_stops = pd.read_sql(query_stops, engine)

if bus_stops.empty:
    print("未找到任何站點資料。")
    exit()

# 用戶輸入起點和終點站名
start_stop = input("請輸入起點站名：").strip().lower()
end_stop = input("請輸入終點站名：").strip().lower()

# 將資料庫中的站名轉為小寫進行匹配
bus_stops['stop_name'] = bus_stops['stop_name'].str.lower()

# 查詢起點和終點的路線
start_routes = bus_stops[bus_stops['stop_name'].str.contains(start_stop)]['route_id'].unique()
end_routes = bus_stops[bus_stops['stop_name'].str.contains(end_stop)]['route_id'].unique()

# 除錯訊息
print(f"起點站名：{start_stop}, 對應路線：{start_routes}")
print(f"終點站名：{end_stop}, 對應路線：{end_routes}")

# 找出同時經過起點和終點的路線
common_routes = set(start_routes) & set(end_routes)

if not common_routes:
    print(f"未找到同時經過 {start_stop} 和 {end_stop} 的公車路線。")
else:
    print(f"以下是同時經過 {start_stop} 和 {end_stop} 的公車路線：")
    for route_id in common_routes:
        # 查詢路線名稱
        query_route_name = f"""
            SELECT route_name 
            FROM data_route_list
            WHERE route_id = '{route_id}'
        """
        route_name = pd.read_sql(query_route_name, engine).iloc[0]['route_name']
        print(f"- {route_name} (Route ID: {route_id})")

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

        # 僅篩選台北市和新北市的資料
        target_cities = ["臺北市", "新北市"]
        filtered_gdf = gdf[gdf["COUNTYNAME"].isin(target_cities)]

        # 從 SQLite 資料庫中讀取所有相關路線的站點座標
        query_stops_for_routes = f"""
            SELECT stop_name, latitude, longitude, route_id
            FROM data_route_info_busstop
            WHERE route_id IN ({','.join([f"'{r}'" for r in common_routes])})
        """
        bus_stops_for_routes = pd.read_sql(query_stops_for_routes, engine)

        if bus_stops_for_routes.empty:
            print("未找到相關路線的站點資料。")
        else:
            # 將站點資料轉換為 GeoDataFrame
            bus_stops_gdf = gpd.GeoDataFrame(
                bus_stops_for_routes,
                geometry=gpd.points_from_xy(bus_stops_for_routes["longitude"], bus_stops_for_routes["latitude"]),
                crs="EPSG:4326"
            )

            # 繪製地圖
            fig, ax = plt.subplots(figsize=(10, 10))
            filtered_gdf.plot(ax=ax, edgecolor='black', color='lightgray', alpha=0.5)
            bus_stops_gdf.plot(ax=ax, color='red', markersize=50, label='Bus Stops')

            plt.title(f"Bus Stops for Routes Passing {start_stop} and {end_stop}")
            plt.axis('equal')
            plt.legend()

            # 儲存地圖為圖片
            output_file = f"bus_stops_{start_stop}_to_{end_stop}.png"
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"地圖已儲存為 {output_file}")

            plt.show()
