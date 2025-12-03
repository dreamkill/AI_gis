import folium
from folium.plugins import MarkerCluster  # 聚合插件，点多的时候会自动聚成一团


def generate_map(data_list, output_file="final_map.html"):
    """
    输入：包含 {"name": "地点名", "coord": (经度, 纬度)} 的列表
    输出：生成 HTML 地图文件
    """
    if not data_list:
        print("没有数据，无法绘图")
        return

    # 1. 计算地图中心点 (所有点的平均值)，保证打开地图时视角正好在数据中心
    avg_lat = sum(d["coord"][1] for d in data_list) / len(data_list)
    avg_lon = sum(d["coord"][0] for d in data_list) / len(data_list)

    # 2. 创建底图
    # location=[纬度, 经度]
    # tiles='CartoDB positron' 是一种非常简洁的灰白色底图，适合学术论文截图，显得很干净
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=14, tiles='CartoDB positron')

    # 3. 添加点位
    # 创建一个聚合组（如果点很多，这一步会让地图很高级）
    marker_cluster = MarkerCluster().add_to(m)

    for item in data_list:
        name = item["name"]
        lon, lat = item["coord"]

        # 添加标记
        folium.Marker(
            location=[lat, lon],  # 注意：这里必须是 [纬度, 经度]
            popup=folium.Popup(name, max_width=300),  # 点击弹出气泡
            tooltip=name,  # 鼠标悬停提示
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(marker_cluster)

    # 4. 保存文件
    m.save(output_file)
    print(f"地图已生成！请用浏览器打开: {output_file}")


# --- 测试数据（假设这是你上一两步跑出来的结果）---
if __name__ == "__main__":
    mock_data = [
        {"name": "武汉光谷广场", "coord": (114.39707, 30.50618)},
        {"name": "华中科技大学", "coord": (114.4138, 30.5146)},
        {"name": "关山大道", "coord": (114.4095, 30.4912)}
    ]

    generate_map(mock_data)