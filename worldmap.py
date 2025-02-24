import json
import streamlit as st
import folium
import geopandas as gpd
import random
from streamlit_folium import folium_static

# 读取世界地图数据
@st.cache_data
def load_map_data():
    world = gpd.read_file("countries.geo.json")  # 读取本地文件
    return world

world = load_map_data()

# 读取国家中英文对照表
@st.cache_data
def load_country_names():
    with open("country_names.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {item["en"]: item["cn"] for item in data}  # 转换为字典 {英文名: 中文名}

country_names = load_country_names()  # 加载中英文国家名称映射

# -------------------- 1. 记忆功能：交互式地图 --------------------
st.title("🌍 记忆世界地图游戏")
st.write("点击地图上的国家，会显示国家的名称（中文 + 英文）。")

# 选择更美观的地图样式
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

# 遍历国家数据并添加到地图
for _, country in world.iterrows():
    name_en = country["name"]  
    name_cn = country_names.get(name_en, name_en)  # 若无匹配，则显示英文

    folium.GeoJson(
        country["geometry"],
        tooltip=f"{name_cn} ({name_en})",
        style_function=lambda x: {
            "fillColor": "#6c5ce7",  # 使用柔和的紫色填充
            "color": "#ffffff",  # 国家边界白色
            "weight": 1,  # 线条宽度
            "fillOpacity": 0.6,  # 透明度
        },
        highlight_function=None  # 取消点击时的黑框
    ).add_to(m)

# 显示地图
folium_static(m)
