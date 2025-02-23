import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
import random
from streamlit_folium import folium_static

# 读取世界地图数据（GeoJSON 格式）
@st.cache_data
def load_map_data():
    world = gpd.read_file("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json")
    return world

world = load_map_data()

# 国家名称映射（部分示例，可扩展）
country_names = {
    "China": "中国",
    "United States": "美国",
    "India": "印度",
    "Brazil": "巴西",
    "Russia": "俄罗斯",
    "Japan": "日本",
    "Germany": "德国",
    "France": "法国",
    "United Kingdom": "英国",
    "Italy": "意大利"
}

# -------------------- 1. 记忆功能：交互式地图 --------------------
st.title("🌍 记忆世界地图游戏")

st.write("点击地图上的国家，会显示国家的名称（中文 + 英文）。")

# 创建地图
m = folium.Map(location=[20, 0], zoom_start=2)

# 添加国家边界，并设置交互（鼠标点击显示国家名）
for _, country in world.iterrows():
    name_en = country["properties"]["name"]
    name_cn = country_names.get(name_en, "未知国家")
    
    folium.GeoJson(
        country["geometry"],
        tooltip=f"{name_cn} ({name_en})",
        style_function=lambda x: {"fillColor": "blue", "color": "black", "weight": 1, "fillOpacity": 0.2}
    ).add_to(m)

# 显示地图
folium_static(m)

# -------------------- 2. 测试功能：选择题 --------------------
st.subheader("🧠 世界地图测试")

# 生成随机测试问题
correct_country = random.choice(list(country_names.keys()))
correct_name_cn = country_names[correct_country]

# 生成 3 个错误选项（不重复）
wrong_countries = random.sample([c for c in country_names.keys() if c != correct_country], 3)
options = wrong_countries + [correct_country]
random.shuffle(options)

# 显示问题
st.write(f"请选择 **{correct_name_cn}**（中文名） 对应的英文国家名：")

# 用户选择答案
selected = st.radio("请选择国家", options)

# 反馈结果
if st.button("提交答案"):
    if selected == correct_country:
        st.success("✅ 正确！")
    else:
        st.error(f"❌ 错误，正确答案是 **{correct_country}** ({correct_name_cn})")

