import os
import streamlit as st
import requests
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
import json

# ✅ 환경 변수 로드
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8090")

# ✅ Streamlit 페이지 설정
st.set_page_config(
    page_title="AI 자기소개서 & 면접 답변 개선 도구",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ CSS 스타일 추가 (세련된 디자인)
st.markdown("""
    <style>
    /* 전체 배경 스타일 */
    .main {
        background-color: #f4f7fc;
        padding: 20px;
        border-radius: 15px;
    }
    
    /* 홈 제목 스타일 */
    .home-title {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .home-subtitle {
    font-size: 1.2rem;
    text-align: center;
    margin-bottom: 40px;
    color: #34495e;
}

    /* AI 피드백 스타일 */
    .feedback-box {
        padding: 20px;
        background: #f9f9f9;
        border-radius: 12px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        font-size: 1.1rem;
        margin-top: 20px;
    }

    /* 피드백 제목 스타일 */
    .feedback-box h3 {
        font-weight: bold;
        font-size: 1.4rem;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    
    .feedback-box h3::before {
        content: "💡";
        font-size: 1.5rem;
        margin-right: 8px;
    }

    /* 피드백 카드 스타일 */
    .feedback-item {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 1.1rem;
    }

    /* 논리적 흐름 */
    .logic-flow {
        background-color: #e3f2fd;
        border-left: 6px solid #42a5f5;
    }

    /* 문법 및 맞춤법 */
    .grammar {
        background-color: #e8f5e9;
        border-left: 6px solid #66bb6a;
    }

    /* 어휘 적절성 */
    .vocabulary {
        background-color: #fff3e0;
        border-left: 6px solid #ff9800;
    }
    /* 카드 스타일 */
    .card-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    .card {
        width: 320px;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease-in-out;
    }
    .card:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 15px rgba(0,0,0,0.2);
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2980b9;
        margin-bottom: 10px;
    }
    .card-icon {
        font-size: 2.5rem;
        color: #6464ff;
        margin-bottom: 10px;
    }
    /* 카드 하단 정렬 */
    .card-bottom {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    /* 질문 박스 (통일된 디자인) */
    .question-box {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 1.1rem;
        background-color: #e3f2fd;  /* 통일된 배경색 */
        border-left: 6px solid #42a5f5;  /* 파란색 강조 */
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 사이드바 메뉴 설정
with st.sidebar:
    menu = option_menu(
        "Menu",
        ["홈 화면", "자기소개서 분석", "면접 답변 피드백", "면접 예상 질문 생성"],
        icons=['house', 'file-text', 'chat-dots', 'list-task'],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={
            "container": {"padding": "5px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#6274CF"},
        }
    )

# ✅ 홈 화면
if menu == "홈 화면":
    st.markdown('<div class="home-title">🏡 AI 자기소개서 & 면접 답변 개선 도구</div>', unsafe_allow_html=True)
    st.markdown('<div class="home-subtitle">AI를 활용한 자기소개서 분석 및 면접 준비 도구입니다.<br>사이드바에서 원하는 기능을 선택하세요.</div>', unsafe_allow_html=True)

    # 카드 UI - 첫 번째 줄 (2개 가로 배치)
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-icon">📝</div>
            <div class="card-title">자기소개서 분석</div>
            <p>AI가 논리적 흐름, 문법, 어휘를 분석하여 피드백을 제공합니다.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🎤</div>
            <div class="card-title">면접 답변 피드백</div>
            <p>면접 답변을 AI가 평가하고 개선 포인트를 제공합니다.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 두 번째 줄 (가운데 정렬)
    st.markdown('<div class="card-bottom">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <div class="card-icon">💡</div>
        <div class="card-title">면접 예상 질문</div>
        <p>지원 직무에 맞는 면접 예상 질문을 AI가 생성합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# ✅ 자기소개서 분석 페이지
elif menu == "자기소개서 분석":
    st.markdown("<h1 style='text-align: center;'>📝 자기소개서 분석</h1>", unsafe_allow_html=True)
    st.markdown("\n\n사용자가 입력한 자기소개서를 분석하여 **논리적 흐름**, **문법**, **어휘 적절성**을 평가합니다.")

    self_intro = st.text_area("✍ 자기소개서를 입력하세요", height=300, placeholder="예) 저는 OO대학교에서 전공을 공부하며 ...")

    if st.button("📊 분석하기"):
        if not self_intro.strip():
            st.warning("⚠ 자기소개서를 입력해주세요!")
        else:
            with st.spinner("🔍 AI가 자기소개서를 분석 중입니다..."):
                response = requests.post(f"{BACKEND_URL}/analyze", json={"user_text": self_intro})

                if response.status_code == 200:
                    try:
                        feedback = response.json().get("feedback", {})
                        logic_flow = feedback.get("logic_flow", "❌ 논리적 흐름 데이터를 가져올 수 없습니다.")
                        grammar = feedback.get("grammar", "❌ 문법 및 맞춤법 데이터를 가져올 수 없습니다.")
                        vocabulary = feedback.get("vocabulary", "❌ 어휘 적절성 데이터를 가져올 수 없습니다.")
                    except Exception as e:
                        logic_flow = grammar = vocabulary = f"⚠ JSON 변환 오류: {str(e)}"
                else:
                    logic_flow = grammar = vocabulary = "❌ 서버 오류 발생"

            st.success("✅ 분석 완료!")

            # ✅ 피드백 UI
            st.markdown(f"""
            <div class="feedback-box">
                <h3>AI 피드백</h3>
                <div class="feedback-item logic-flow">✅ <strong>논리적 흐름:</strong> {logic_flow}</div>
                <div class="feedback-item grammar">✅ <strong>문법 및 맞춤법:</strong> {grammar}</div>
                <div class="feedback-item vocabulary">🔧 <strong>어휘 적절성:</strong> {vocabulary}</div>
            </div>
            """, unsafe_allow_html=True)

# ✅ 면접 답변 피드백 페이지
elif menu == "면접 답변 피드백":
    st.title("🎤 면접 답변 피드백")

    interview_response = st.text_area("✍ 면접 답변을 입력하세요", height=300, placeholder="Q: 질문\n A: 답변")

    if st.button("📊 분석하기"):
        if not interview_response.strip():
            st.warning("⚠ 면접 답변을 입력해주세요!")
        else:
            with st.spinner("🔍 AI가 면접 답변을 분석 중입니다..."):
                response = requests.post(f"{BACKEND_URL}/qanda", json={"user_text": interview_response})

                if response.status_code == 200:
                    feedback = response.json().get("feedback", {})
                    strength = feedback.get("strength", "❌ 강점 분석 데이터를 가져올 수 없습니다.")
                    weakness = feedback.get("weakness", "❌ 약점 분석 데이터를 가져올 수 없습니다.")
                    improvement = feedback.get("improvement", "❌ 개선 사항 데이터를 가져올 수 없습니다.")
                else:
                    strength = weakness = improvement = "❌ 서버 오류 발생"

            st.success("✅ 분석 완료!")

            # ✅ 피드백 UI
            st.markdown(f"""
            <div class="feedback-box">
                <h3>AI 피드백</h3>
                <div class="feedback-item logic-flow">✅ <strong>강점 분석:</strong> {strength}</div>
                <div class="feedback-item grammar">✅ <strong>약점 분석:</strong> {weakness}</div>
                <div class="feedback-item vocabulary">🔧 <strong>개선 사항:</strong> {improvement}</div>
            </div>
            """, unsafe_allow_html=True)
# ✅ 면접 예상 질문 생성
elif menu == "면접 예상 질문 생성":
    st.title("📝 면접 예상 질문 생성")
    st.markdown("지원하실 **직종/회사** 정보와 예상 **질문 개수**를 입력하면, AI가 예상 질문을 생성합니다.")

    job_info = st.text_area("지원하실 **직종/회사** 정보를 입력하세요", height=200, placeholder="예) IT기업, 소프트웨어 엔지니어 지원")
    question_count = st.number_input("예상 질문 개수", min_value=1, max_value=10, value=5, step=1)

    if st.button("📊 질문 생성하기"):
        if not job_info.strip():
            st.warning("⚠ 지원 정보를 입력해주세요!")
        else:
            with st.spinner("질문을 생성하는 중..."):
                try:
                    print(f"🔎 요청된 질문 개수: {question_count}")
                    response = requests.post(f"{BACKEND_URL}/mkq", json={"user_text": job_info, "question_count": question_count})

                    # 🔍 원본 응답 출력 (디버깅용)
                    print(f"🔎 AI 응답 원본: {response.text}")

                    # ✅ JSON 변환 시도 (이제 `response.json()` 직접 사용)
                    if response.status_code == 200:
                        data = response.json()  # AI 응답을 JSON으로 변환
                        questions = data.get("feedback", {}).get("questions", [])  # 질문 리스트 가져오기

                        questions = questions[:question_count]  
                        if not questions:
                            questions = ["❌ 질문을 생성할 수 없습니다. 다시 시도해주세요."]
                    
                    else:
                        questions = ["❌ 서버 오류가 발생했습니다."]
                
                except requests.exceptions.RequestException as e:
                    print(f"❌ 요청 오류: {e}")
                    questions = ["❌ 서버 요청 중 오류가 발생했습니다."]
                
                except json.JSONDecodeError as e:
                    print(f"❌ JSON 변환 오류: {e}")
                    questions = [f"❌ JSON 변환 오류: {str(e)}"]

            st.success("✅ 질문 생성 완료!")
            # ✅ 면접 예상 질문 피드백 UI (질문 박스만 존재하도록 수정)
            question_list_html = "".join([
                f"<li><strong>Q{idx}:</strong> {question}</li>" for idx, question in enumerate(questions, start=1)
            ])

            st.markdown(f"""
                <div class="feedback-box">
                    <h3>AI 면접 예상 질문</h3>
                    <ul class="question-list">
                        {question_list_html}
                    </ul>
                </div>
            """, unsafe_allow_html=True)