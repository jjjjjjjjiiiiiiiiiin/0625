import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# 앱 제목
st.title("서울시 고등학교 학년별 학급 수 지도")

# CSV 불러오기
df = pd.read_csv("2025년도_학년별 학급별 학생수(고)_전체.csv", encoding='utf-8')

# 구 이름 통일 (공백 제거 등)
df['자치구'] = df['자치구'].str.strip()

# 학년 선택
학년목록 = [col for col in df.columns if '학급수' in col]
선택학년 = st.sidebar.selectbox("학년 선택", 학년목록)

# 학급 수 집계 (구별로)
grouped = df.groupby('자치구')[선택학년].sum().reset_index()

# 서울시 구 경계 geojson (서울시 행정구역)
@st.cache_data
def load_geo():
    url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/seoul_municipalities_geo_simple.json"
    return gpd.read_file(url)

geo_df = load_geo()

# Folium 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# Choropleth (단계 구분도)
choropleth = folium.Choropleth(
    geo_data=geo_df,
    name="choropleth",
    data=grouped,
    columns=["자치구", 선택학년],
    key_on="feature.properties.name",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"{선택학년} (학급 수)",
).add_to(m)

# 팝업 추가
folium.LayerControl().add_to(m)

# 지도 출력
st.subheader(f"선택한 학년: {선택학년}")
st_data = st_folium(m, width=700, height=500)

# 데이터 표 출력
st.subheader("구별 학급 수 데이터")
st.dataframe(grouped)
