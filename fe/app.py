import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI 자기소개서 & 면접 답변 개선 도구", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.title("AI 자기소개서 & 면접 답변 개선 도구")

def analyze_self_intro():
    st.header("✅ 자기소개서 분석 및 개선")
    st.markdown("사용자가 입력한 자기소개서를 분석하여 **논리적 흐름**, **문법**, **어휘 적절성**을 평가합니다.")
    self_intro = st.text_area("자기소개서를 입력하세요", height=350, placeholder="예) 저는 OO대학교에서 전공을 공부하며 ...")
    
    if st.button("분석하기", key="self_intro"):
        with st.spinner("자기소개서를 분석하는 중..."):
            response = requests.post(f"{BACKEND_URL}/analyze", json={"user_text": self_intro})
            if response.status_code == 200:
                feedback = response.json().get("feedback", "분석 결과를 가져올 수 없습니다.")
            else:
                feedback = "서버 오류가 발생했습니다."
        
        st.success("분석 완료!")
        st.subheader("AI 피드백")
        st.markdown(feedback)

def interview_feedback():
    st.header("✅ 면접 답변 피드백")
    interview_answer = st.text_area("면접 답변을 입력하세요", height=300, placeholder="예) 제 강점은 ...")
    
    if st.button("분석하기", key="interview"):
        with st.spinner("면접 답변을 분석하는 중..."):
            response = requests.post(f"{BACKEND_URL}/analyze", json={"user_text": interview_answer})
            if response.status_code == 200:
                feedback = response.json().get("feedback", "분석 결과를 가져올 수 없습니다.")
            else:
                feedback = "서버 오류가 발생했습니다."
        
        st.success("분석 완료!")
        st.subheader("AI 피드백")
        st.markdown(feedback)

def main():
    menu = st.sidebar.radio("메뉴 선택", 
                             ("자기소개서 분석 및 개선", "면접 답변 피드백"))
    
    if menu == "자기소개서 분석 및 개선":
        analyze_self_intro()
    elif menu == "면접 답변 피드백":
        interview_feedback()

if __name__ == "__main__":
    main()
