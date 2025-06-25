#import streamlit as st

#st.title("📊 전국 고등학교 학생 분석")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 웹앱 제목
st.title("2025년도 시도교육청별 학급당 학생 수")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("2025년도_학년별·학급별 학생수(고)_전체.csv", encoding='utf-8')
    return df

df = load_data()

# 데이터 확인
st.subheader("원본 데이터 (일부 보기)")
st.dataframe(df.head())

# 시도교육청 컬럼명 추정
지역_컬럼 = [col for col in df.columns if '시도' in col or '지역' in col or '교육청' in col]
if 지역_컬럼:
    지역_컬럼명 = 지역_컬럼[0]
else:
    st.error("시도교육청(지역) 정보를 가진 컬럼을 찾을 수 없습니다.")
    st.stop()

# 학급 수와 학생 수 컬럼 추정
학급수_컬럼 = [col for col in df.columns if '학급수' in col]
학생수_컬럼 = [col for col in df.columns if '학생수' in col and '계' in col]

if not 학급수_컬럼 or not 학생수_컬럼:
    st.error("학급 수 또는 학생 수 컬럼이 부족합니다.")
    st.stop()

# 집계 및 계산
grouped = df.groupby(지역_컬럼명)[학생수_컬럼[0], 학급수_컬럼[0]].sum().reset_index()
grouped["학급당 학생수"] = grouped[학생수_컬럼[0]] / grouped[학급수_컬럼[0]]

# 정렬
grouped = grouped.sort_values("학급당 학생수", ascending=False)

# 그래프 출력
st.subheader("지역별 학급당 학생 수")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(grouped[지역_컬럼명], grouped["학급당 학생수"], color='skyblue')
ax.set_ylabel("학급당 학생 수")
ax.set_xlabel("시도교육청")
ax.set_title("시도교육청별 학급당 학생 수")
plt.xticks(rotation=45)

# 숫자 표시
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f"{yval:.1f}", ha='center', va='bottom')

st.pyplot(fig)
