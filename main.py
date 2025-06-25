#import streamlit as st

#st.title("📊 전국 고등학교 학생 분석")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="서울시 고등학교 분석", layout="wide")

st.title("📊 서울시 자치구별 학급당 학생 수 (고등학교)")

# ✅ 업로드한 파일 직접 경로로 불러오기
file_path = "/mnt/data/2025년도_학년별·학급별 학생수(고)_전체.csv"
df = pd.read_csv(file_path, encoding='utf-8')

# ✅ '서울' 포함된 행만 필터링
서울_df = df[df.apply(lambda row: row.astype(str).str.contains("서울"), axis=1)]

# ✅ 자치구 추출 (학교명 또는 지역명 컬럼에서 'xx구')
후보컬럼 = [col for col in 서울_df.columns if '학교명' in col or '지역명' in col or '주소' in col]
구_컬럼 = None

for col in 후보컬럼:
    if 서울_df[col].astype(str).str.contains('구').any():
        구_컬럼 = col
        break

if 구_컬럼:
    서울_df['자치구'] = 서울_df[구_컬럼].astype(str).str.extract(r'(\w+구)')
else:
    st.error("자치구 정보를 추출할 수 있는 컬럼이 없습니다.")
    st.stop()

# ✅ 학급수 / 학생수 컬럼 찾기
학급수_컬럼 = [col for col in df.columns if '학급수' in col][0]
학생수_컬럼 = [col for col in df.columns if '학생수' in col and '계' in col][0]

# ✅ 자치구별 집계
grouped = 서울_df.groupby('자치구')[[학생수_컬럼, 학급수_컬럼]].sum()
grouped['학급당 학생수'] = grouped[학생수_컬럼] / grouped[학급수_컬럼]
grouped = grouped.dropna().sort_values('학급당 학생수', ascending=False)

# ✅ 시각화
st.subheader("🧮 자치구별 학급당 학생 수 비교")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(grouped.index, grouped['학급당 학생수'], color='lightblue')
ax.set_ylabel("학급당 학생 수")
ax.set_xlabel("자치구")
ax.set_title("서울시 자치구별 학급당 학생 수")
plt.xticks(rotation=45)
for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.3, f"{y:.1f}", ha='center', fontsize=9)
st.pyplot(fig)
