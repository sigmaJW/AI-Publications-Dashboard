import streamlit as st
import pandas as pd
import altair as alt

# ----------------------------------
# 1. 페이지 설정
# ----------------------------------
st.set_page_config(
    page_title="AI Publications Dashboard",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------
# 2. 제목 및 설명
# ----------------------------------
st.title("🤖 Global AI Publications Dashboard")
st.markdown(
    """
    이 대시보드는 **국가별 AI 논문 발표 추이**를 시각적으로 보여줍니다.  
    데이터는 *Our World in Data - Annual Scholarly Publications on Artificial Intelligence*를 기반으로 합니다.
    """
)

# ----------------------------------
# 3. 파일 업로드
# ----------------------------------
uploaded = "ai_publications.csv"

# ----------------------------------
# 4. 데이터 불러오기
# ----------------------------------
try:
    df = pd.read_csv(uploaded)
except Exception as e:
    st.error(f"파일을 불러오는 중 오류 발생: {e}")
    st.stop()

# ----------------------------------
# 5. 데이터 정제 및 확인
# ----------------------------------
if "code" not in df.columns or "entity" not in df.columns or "year" not in df.columns:
    st.error("❌ 필수 열(entity, code, year)이 없습니다. 올바른 CSV 파일을 업로드하세요.")
    st.stop()

# 결측치 제거
df = df.dropna(subset=["code"])

# ----------------------------------
# 6. 사용자 인터페이스 (국가 선택)
# ----------------------------------
countries = sorted(df["entity"].unique())
selected_countries = st.multiselect(
    "🌐 분석할 국가를 선택하세요 (최대 5개 추천)",
    countries,
    default=countries[:3]
)

if not selected_countries:
    st.warning("국가를 최소 하나 이상 선택하세요.")
    st.stop()

# 선택된 데이터 필터링
filtered_df = df[df["entity"].isin(selected_countries)]

# ----------------------------------
# 7. 연도별 논문 수 시각화
# ----------------------------------
line_chart = (
    alt.Chart(filtered_df)
    .mark_line(point=True, interpolate="monotone")
    .encode(
        x=alt.X("year:O", title="연도"),
        y=alt.Y("value:Q", title="AI 논문 수"),
        color=alt.Color("entity:N", title="국가"),
        tooltip=["entity", "year", "value"]
    )
    .properties(
        title="📈 연도별 AI 논문 수 추이",
        width=800,
        height=400
    )
    .configure_title(fontSize=18, anchor="start", color="#333")
    .interactive()
)

# ----------------------------------
# 8. 최근 연도 TOP 10 국가 시각화
# ----------------------------------
latest_year = filtered_df["year"].max()
top10 = (
    df[df["year"] == latest_year]
    .nlargest(10, "value")[["entity", "value"]]
)

bar_chart = (
    alt.Chart(top10)
    .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
    .encode(
        x=alt.X("entity:N", sort='-y', title="국가"),
        y=alt.Y("value:Q", title=f"{latest_year}년 AI 논문 수"),
        color=alt.Color("value:Q", scale=alt.Scale(scheme="tealblues")),
        tooltip=["entity", "value"]
    )
    .properties(
        title=f"🏆 {latest_year}년 AI 논문 수 TOP 10 국가",
        width=800,
        height=400
    )
)

# ----------------------------------
# 9. 시각화 출력
# ----------------------------------
st.altair_chart(line_chart, use_container_width=True)
st.altair_chart(bar_chart, use_container_width=True)

# ----------------------------------
# 10. 요약 정보
# ----------------------------------
st.subheader("📊 데이터 요약")
col1, col2 = st.columns(2)
with col1:
    st.metric("분석된 국가 수", f"{df['entity'].nunique()}개국")
with col2:
    st.metric("데이터 연도 범위", f"{int(df['year'].min())} ~ {int(df['year'].max())}")

st.dataframe(filtered_df.head(10), use_container_width=True)

# ----------------------------------
# 11. 하단 설명
# ----------------------------------
st.markdown("---")
st.caption("© 2025 AI Publications Dashboard | Built with Streamlit + Altair 🎨")
