import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import matplotlib

# 關閉 matplotlib 的互動模式
matplotlib.use('Agg')


def draw_geojson_to_png(inputfile: str, outputfile: str):
    """
    繪製靜態地圖並儲存為 PNG 檔案
    :param inputfile: GeoJSON 檔案路徑
    :param outputfile: 輸出的 PNG 檔案路徑
    """
    # 讀取指定的 GeoJSON 檔案
    bus_stops = gpd.read_file(inputfile)

    # 繪製所有公車站點 (靜態地圖)
    fig, ax = plt.subplots(figsize=(10, 10))
    bus_stops.plot(ax=ax, color='blue', markersize=5)
    plt.title("Bus Stops")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # 儲存為指定的 PNG 檔案
    plt.savefig(outputfile)
    plt.close()


def draw_geojson_to_html(inputfile: str, outputfile: str):
    """
    繪製互動地圖並儲存為 HTML 檔案
    :param inputfile: GeoJSON 檔案路徑
    :param outputfile: 輸出的 HTML 檔案路徑
    """
    # 讀取指定的 GeoJSON 檔案
    bus_stops = gpd.read_file(inputfile)

    # 設定地圖中心為所有站點的中心點
    center = [bus_stops.geometry.y.mean(), bus_stops.geometry.x.mean()]
    m = folium.Map(location=center, zoom_start=13)

    # 將所有站點加入地圖
    for _, row in bus_stops.iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"座標: ({row.geometry.y:.6f}, {row.geometry.x:.6f})"
        ).add_to(m)

    # 儲存互動地圖為 HTML 檔案
    m.save(outputfile)


if __name__ == "__main__":
    # 指定輸入的 GeoJSON 檔案和輸出的檔案
    inputfile = "20250422/bus_stops.geojson"
    output_png = "bus_stops.png"
    output_html = "bus_stops.html"

    # 繪製靜態地圖並儲存
    draw_geojson_to_png(inputfile, output_png)

    # 繪製互動地圖並儲存
    draw_geojson_to_html(inputfile, output_html)

    print("完成！靜態地圖儲存為 bus_stops.png，互動地圖儲存為 bus_stops.html")