#import streamlit as st

#st.title("📊 전국 고등학교 학생 분석")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import chardet  # 인코딩 감지용

st.title("📊 서울시 자치구별 학급당 학생 수 (고등학교)")

# 업로드한 파일 경로
file_path = "/2025년도_학년별·학급별 학생수(고)_전체.csv"

# ✅ 인코딩 자동 감지
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))  # 앞부분 10KB 샘플
        return result['encoding']

# ✅ 파일 읽기
try:
    encoding = detect_encoding(file_path)
    df = pd.read_csv(file_path, encoding=encoding)
    st.success(f"파일 불러오기 성공 ✅ (인코딩: {encoding})")
except Exception as e:
    st.error(f"파일을 불러오는 데 실패했습니다: {e}")
    st.stop()

# ▶ 서울시 데이터만 필터링
서울_df = df[df.apply(lambda row: row.astype(str).str.contains("서울"), axis=1)]

# ▶ 자치구 추출
구_컬럼 = None
for col in df.columns:
    if df[col].astype(str).str.contains("구").any():
        구_컬럼 = col
        break

if 구_컬럼:
    서울_df['자치구'] = 서울_df[구_컬럼].astype(str).str.extract(r'(\w+구)')
else:
    st.error("자치구 정보를 찾을 수 없습니다.")
    st.stop()

# ▶ 학급수 / 학생수 컬럼 찾기
학급수_컬럼 = [col for col in df.columns if '학급수' in col][0]
학생수_컬럼 = [col for col in df.columns if '학생수' in col and '계' in col][0]

# ▶ 통계 계산
grouped = 서울_df.groupby('자치구')[[학생수_컬럼, 학급수_컬럼]].sum()
grouped['학급당 학생수'] = grouped[학생수_컬럼] / grouped[학급수_컬럼]
grouped = grouped.dropna().sort_values('학급당 학생수', ascending=False)

# ▶ 그래프
st.subheader("서울시 자치구별 학급당 학생 수")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(grouped.index, grouped['학급당 학생수'], color='cornflowerblue')
ax.set_title("서울시 자치구별 학급당 학생 수")
plt.xticks(rotation=45)
for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.5, f"{y:.1f}", ha='center')
st.pyplot(fig)
