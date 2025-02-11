import streamlit as st
import requests
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8090")

st.set_page_config(
    page_title="AI 자기소개서 & 면접 답변 개선 도구",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("AI 자기소개서 & 면접 답변 개선 도구")

# --- 세션 상태 초기화 ---
if "menu" not in st.session_state:
    st.session_state["menu"] = "Home"

# --- 사이드바 ---
st.sidebar.title("📂 메뉴 선택")

# 메뉴 리스트
menu_items = {
    "Home": "🏠 홈 화면",
    "SelfIntro": "📝 자기소개서 분석",
    "Interview": "🎤 면접 답변 피드백"
}

# 사이드바 버튼을 활용한 메뉴 선택
for key, label in menu_items.items():
    if st.sidebar.button(label, key=key):
        st.session_state["menu"] = key  # 버튼 클릭 시 메뉴 변경

# --- 각 메뉴에 따른 화면 구성 ---
if st.session_state["menu"] == "Home":
    st.title("🏠 홈 화면")
    st.write("환영합니다! AI 자기소개서 및 면접 분석 도구입니다.")
    st.markdown("사이드바에서 원하는 기능을 선택하세요.")

elif st.session_state["menu"] == "SelfIntro":
    st.title("📝 자기소개서 분석")
    st.markdown("사용자가 입력한 자기소개서를 분석하여 **논리적 흐름**, **문법**, **어휘 적절성**을 평가합니다.")
    
    self_intro = st.text_area("자기소개서를 입력하세요", height=300, placeholder="예) 저는 OO대학교에서 전공을 공부하며 ...")

    if st.button("📊 분석하기"):
        if not self_intro.strip():
            st.warning("⚠ 자기소개서를 입력해주세요!")
        else:
            with st.spinner("자기소개서를 분석하는 중..."):
                response = requests.post(f"{BACKEND_URL}/analyze", json={"user_text": self_intro})
                if response.status_code == 200:
                    feedback = response.json().get("feedback", "분석 결과를 가져올 수 없습니다.")
                else:
                    feedback = "서버 오류가 발생했습니다."

            st.success("✅ 분석 완료!")
            st.subheader("AI 피드백")
            st.markdown(feedback)

elif st.session_state["menu"] == "Interview":
    st.title("🎤 면접 답변 피드백")
    st.markdown("면접 답변을 분석하여 **논리적 흐름**, **문법**, **어휘 적절성**을 평가합니다.")
    
    interview_response = st.text_area("면접 답변을 입력하세요", height=250, placeholder="예) 제 강점은 ...")

    if st.button("🎙 분석하기"):
        if not interview_response.strip():
            st.warning("⚠ 면접 답변을 입력해주세요!")
        else:
            with st.spinner("면접 답변을 분석하는 중..."):
                response = requests.post(f"{BACKEND_URL}/qanda", json={"user_text": interview_response})
                if response.status_code == 200:
                    feedback = response.json().get("feedback", "분석 결과를 가져올 수 없습니다.")
                else:
                    feedback = "서버 오류가 발생했습니다."

            st.success("✅ 분석 완료!")
            st.subheader("AI 피드백")
            st.markdown(feedback)
