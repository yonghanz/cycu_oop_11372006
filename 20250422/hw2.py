import json
import folium
import os


def geojson_to_html(geojson_file, output_html):
    """
    Converts a GeoJSON file into an interactive HTML map using Folium.

    :param geojson_file: Path to the input GeoJSON file.
    :param output_html: Path to the output HTML file.
    """
    # 檢查檔案是否存在
    if not os.path.exists(geojson_file):
        print(f"檔案不存在：{geojson_file}")
        return

    # Load GeoJSON data
    with open(geojson_file, 'r', encoding='utf-8') as file:
        geojson_data = json.load(file)

    # 計算地圖中心點
    first_feature = geojson_data['features'][0]
    coordinates = first_feature['geometry']['coordinates']
    if first_feature['geometry']['type'] == 'Point':
        center_lat, center_lon = coordinates[1], coordinates[0]
    else:
        center_lat, center_lon = coordinates[0][1], coordinates[0][0]

    # Create a Folium map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # Add GeoJSON data to the map with styles
    folium.GeoJson(
        geojson_data,
        style_function=lambda x: {
            'fillColor': 'blue',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.5,
        }
    ).add_to(m)

    # Save the map to an HTML file
    m.save(output_html)
    print(f"互動地圖已儲存為：{output_html}")


if __name__ == "__main__":
    # 指定輸入的 GeoJSON 檔案和輸出的 HTML 檔案
    inputfile = "20250422/bus_stops.geojson"
    outputfile = "bus_stops.html"

    # 繪製並儲存圖形
    geojson_to_html(inputfile, outputfile)