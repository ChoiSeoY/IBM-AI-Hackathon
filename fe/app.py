import streamlit as st
import time
import os
import sys
import subprocess

# 페이지 설정 및 기본 CSS 스타일링 (배경, 글자색, 사이드바 등)
st.set_page_config(
    page_title="AI 자기소개서 & 면접 답변 개선 도구", 
    layout="wide", 
    initial_sidebar_state="expanded"
    )
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .appview-container {
        background: #ffffff;
    }
     /* 텍스트 스타일 - 가독성 개선 */
    h1 { font-size: 2rem; color: #212529; font-weight: bold; }
    h2 { font-size: 1.75rem; color: #343a40; }
    h3 { font-size: 1.5rem; color: #495057; }
    h4 { font-size: 1.25rem; color: #6c757d; }
    body { line-height: 1.5; font-size: 1rem; color: #495057; }
    }
    .sidebar {
        background-color: #e9ecef;
        padding: 20px;
    }
    .stSidebar h2 {
        font-size: 1.5rem;
        font-weight: bold;
    }
     .stSidebar .stButton, .stSidebar .stTextInput, .stSidebar .stSelectbox {
        margin-bottom: 15px;
    }
    .stButton>button {
        background-color: #007bff;
        color: #ffffff;
        border: none;
        padding: 0.7em 1.2em;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        backgroud-color: #0056b3;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- 기능별 페이지 함수 정의 ---

def analyze_self_intro():
    st.header("✅ 자기소개서 분석 및 개선")
    st.markdown("사용자가 입력한 자기소개서를 분석하여 **논리적 흐름**, **문법**, **어휘 적절성**을 평가합니다.<br>Watsonx.ai 기반의 피드백과 개선된 예시를 확인해보세요.", unsafe_allow_html=True)
    self_intro = st.text_area(
    "자기소개서를 입력하세요",
    height=350,
    placeholder="예) 저는 OO대학교에서 전공을 공부하며 ...",
)
    if st.button("분석하기", key="self_intro"):
        with st.spinner("자기소개서를 분석하는 중..."):
            time.sleep(2)  # 실제 API 호출 시 대체
            # 여기에 Watsonx.ai API 연동 로직 추가 가능
            feedback = (
                "- **논리적 흐름:** 전반적으로 일관성이 있으나, 중간 부분에서 연결이 매끄럽지 않은 구간이 있습니다.\n"
                "- **문법:** 일부 문장에서 조사 사용에 오류가 있습니다. 예를 들어, '나는 경험있다' → '경험이 있다'로 수정 권장합니다.\n"
                "- **어휘:** 보다 전문적이고 다양한 어휘 사용이 필요합니다."
            )
        st.success("분석 완료!")
        
        st.subheader("AI 피드백")
        st.markdown(feedback)
        
        st.subheader("개선된 자기소개서 예시")
        improved_text = "여기에 Watsonx.ai 기반의 개선된 자기소개서 예시가 표시됩니다."
        st.text_area("개선된 자기소개서", improved_text, height=200)
        
        st.subheader("키워드 강조 및 핵심 문장 추천")
        st.markdown("**추천 키워드:** 경험, 열정, 전문성")
        st.markdown("**핵심 문장 예시:** '저는 다양한 프로젝트를 통해 문제 해결 능력을 극대화하였습니다.'")

def interview_feedback():
    st.header("✅ 면접 답변 피드백")
    st.markdown("입력한 면접 답변을 AI가 분석하여 **더 나은 답변**을 추천합니다.<br>특정 면접 질문에 대한 모범 답변과 예상 질문도 함께 제공합니다.", unsafe_allow_html=True)
    
    interview_answer = st.text_area("면접 답변을 입력하세요", height=300, placeholder="예) 제 강점은 ...")
    if st.button("분석하기", key="interview"):
        with st.spinner("면접 답변을 분석하는 중..."):
            time.sleep(2)  # 실제 API 호출 시 대체
            # Watsonx.ai API를 통한 답변 피드백 로직 구현 가능
            feedback = (
                "- **명확성:** 답변이 전체적으로 전달되지만, 구체적인 사례 제시가 부족합니다.\n"
                "- **구성:** 답변의 시작 부분에서 보다 강한 인상을 남길 필요가 있습니다."
            )
        st.success("분석 완료!")
        
        st.subheader("AI 피드백")
        st.markdown(feedback)
        
        st.subheader("개선된 면접 답변 예시")
        improved_answer = "여기에 Watsonx.ai 기반의 모범 면접 답변 예시가 표시됩니다."
        st.text_area("개선된 면접 답변", improved_answer, height=200)
        
        st.subheader("면접 예상 질문 추천")
        st.markdown("1. 자신의 강점과 약점은 무엇인가요?\n2. 지원 동기는 무엇인가요?")

def audio_feedback():
    st.header("✅ 음성 피드백 (추후 확장)")
    st.markdown("사용자의 음성 녹음을 분석하여 **발음**, **억양**, **속도** 등을 평가합니다.<br>현재는 파일 업로드 후 간단한 피드백을 제공하는 기능을 준비 중입니다.", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("음성 파일 업로드 (mp3, wav)", type=["mp3", "wav"])
    if uploaded_file is not None:
        st.audio(uploaded_file)
        if st.button("분석하기", key="audio"):
            with st.spinner("음성 분석 중..."):
                time.sleep(2)  # 실제 음성 분석 API 연동 시 대체
            st.success("분석 완료!")
            st.markdown("**발음:** 90점\n**억양:** 85점\n**속도:** 88점")
    else:
        st.info("분석을 위해 음성 파일을 업로드 해주세요.")

def resume_template():
    st.header("✅ 이력서 및 지원서 템플릿 제공")
    st.markdown("직무별 최적화된 **이력서 및 자기소개서 템플릿**을 제공합니다.<br>원하는 직무를 선택하여 예시 템플릿과 추천 문장을 확인해보세요.", unsafe_allow_html=True)
    
    job_category = st.selectbox("직무 선택", [
        "개발자", "마케터", "디자이너", "데이터 분석가", 
        "프로젝트 매니저", "영업 전문가", "인사 담당자", 
        "회계 전문가", "교육 전문가", "연구원"
    ])
    
    if job_category == "개발자":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-1234-5678 / email@example.com
- **경력 요약:** 5년 이상의 웹 및 소프트웨어 개발 경험 보유
- **기술 스택:** Python, JavaScript, React, Node.js, SQL 등
- **주요 프로젝트:** e-Commerce 플랫폼, SaaS 애플리케이션 개발
- **문제 해결 사례:** 복잡한 버그 및 성능 이슈 해결 경험
- **협업 경험:** 크로스펑셔널 팀과의 효과적인 협업
- **교육 및 인증:** 정보처리기사, 부트캠프 수료 등
- **포트폴리오:** GitHub 및 개인 웹사이트 링크 제공
- **기타 활동:** 코드 리뷰, 기술 블로그 운영, 오픈 소스 기여
        """)
    elif job_category == "마케터":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-2345-6789 / email@example.com
- **경력 요약:** 디지털 마케팅 및 브랜드 전략 경력 7년 이상
- **전문 분야:** 디지털 광고, SEO, SNS, 콘텐츠 마케팅
- **주요 캠페인:** 브랜드 런칭, 매출 증대 성공 사례 다수
- **분석 능력:** 마케팅 성과 분석 및 데이터 기반 의사결정
- **창의적 전략:** 혁신적인 마케팅 전략 수립 및 실행
- **커뮤니케이션:** 고객 및 팀원과의 원활한 소통
- **교육 및 인증:** Google Analytics, Facebook Blueprint 등
- **기타 활동:** 시장 트렌드 분석, 세미나 발표 및 워크숍 참여
        """)
    elif job_category == "디자이너":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-3456-7890 / email@example.com
- **전문 분야:** UX/UI 디자인, 그래픽 디자인, 브랜딩
- **사용 툴:** Adobe Creative Suite, Sketch, Figma 등
- **포트폴리오:** 웹 기반 포트폴리오 및 Dribbble/Behance 링크
- **프로젝트 경험:** 다양한 디지털 및 인쇄 디자인 프로젝트 수행
- **디자인 철학:** 사용자 중심의 심미적 디자인 구현
- **협업 경험:** 개발자, 마케터와의 크로스 팀 협업
- **수상 경력:** 디자인 공모전 및 콘테스트 수상 경험
- **기타 활동:** 최신 디자인 트렌드 연구 및 세미나 발표
        """)
    elif job_category == "데이터 분석가":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-4567-8901 / email@example.com
- **경력 요약:** 데이터 분석 및 시각화 경력 4년 이상
- **분석 도구:** Python, R, SQL, Tableau, Power BI 등
- **데이터 시각화:** 복잡한 데이터 셋 시각화 프로젝트 사례
- **통계 분석:** 회귀분석, 분산분석 등 다양한 통계 기법 활용
- **문제 해결:** 데이터 기반 비즈니스 문제 해결 경험
- **협업 경험:** 부서간 협업을 통한 데이터 공유 및 분석
- **교육:** 통계학 또는 관련 분야 학위 소지
- **자격증:** 데이터 분석 관련 인증 및 수료증 보유
        """)
    elif job_category == "프로젝트 매니저":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-5678-9012 / email@example.com
- **경력 요약:** 프로젝트 관리 및 팀 리딩 경험 6년 이상
- **주요 프로젝트:** 대규모 IT 및 서비스 론칭 프로젝트 관리
- **일정 관리:** 마일스톤 설정 및 진행 상황 모니터링 경험
- **리더십:** 팀원 동기 부여 및 성과 극대화 전략 수립
- **위험 관리:** 리스크 평가 및 대응 전략 마련
- **커뮤니케이션:** 이해관계자와의 효과적인 소통
- **자격증:** PMP, Prince2 등 국제 인증 보유
- **성과 기록:** 프로젝트 성과 및 비용 절감 실적 보유
        """)
    elif job_category == "영업 전문가":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-6789-0123 / email@example.com
- **경력 요약:** 영업 및 고객 관리 경력 5년 이상
- **판매 성과:** 분기별, 연간 매출 목표 초과 달성 경험
- **주요 고객:** 주요 고객 및 거래처 관리 사례 다수
- **영업 전략:** 시장 분석 기반 영업 전략 수립 및 실행
- **커뮤니케이션:** 고객 신뢰 구축 및 관계 유지 능력
- **팀워크:** 팀 내 협업 및 신규 고객 발굴 경험
- **성과 보상:** 영업 인센티브 및 수상 경력 보유
- **기타 활동:** 신규 시장 개척 및 고객 피드백 반영 전략
        """)
    elif job_category == "인사 담당자":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-7890-1234 / email@example.com
- **경력 요약:** 인사 관리 및 조직 개발 경력 4년 이상
- **채용 프로세스:** 인재 발굴 및 선발 프로세스 운영 경험
- **교육 프로그램:** 신규 직원 교육 프로그램 기획 및 운영
- **성과 평가:** 공정한 성과 평가 및 보상 체계 구축
- **노사 관계:** 갈등 해결 및 원만한 노사 관계 유지 경험
- **조직문화:** 조직 문화 개선 및 직원 만족도 향상 전략
- **자격증:** HR 관련 자격증 (HRD, PHR 등) 보유
- **기타 활동:** 인사 전략 기획 및 HR 데이터 분석 경험
        """)
    elif job_category == "회계 전문가":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-8901-2345 / email@example.com
- **경력 요약:** 회계 및 재무 관리 경력 7년 이상
- **재무 분석:** 재무제표 분석 및 예측 업무 수행
- **회계 소프트웨어:** ERP, QuickBooks, SAP 등 사용 경험
- **세무 관리:** 세무 신고 및 절세 전략 수립 경험
- **감사 대응:** 내부/외부 감사 대응 및 준비 경험
- **자산 관리:** 기업 자산 관리 및 리스크 평가 사례
- **교육:** 회계학 전공 및 관련 학위 소지
- **자격증:** 공인회계사(CPA) 등 전문 자격 보유
        """)
    elif job_category == "교육 전문가":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-9012-3456 / email@example.com
- **경력 요약:** 교육 및 강의 경력 5년 이상
- **교육 철학:** 학생 중심의 혁신적 교육 접근법
- **수업 경험:** 다양한 과목 및 학년 대상 수업 진행
- **교육 과정 설계:** 커리큘럼 개발 및 교육 프로그램 운영
- **학생 평가:** 효과적인 평가 및 피드백 시스템 구축
- **교육 기술:** 최신 교육 기술 및 온라인 플랫폼 활용
- **자격증:** 교원 자격증 및 관련 교육 인증 보유
- **기타 활동:** 워크숍, 세미나, 교육 관련 발표 경험
        """)
    elif job_category == "연구원":
        st.markdown("""
- **이름:** 홍길동
- **연락처:** 010-0123-4567 / email@example.com
- **경력 요약:** 연구 및 학술 활동 경력 4년 이상
- **연구 분야:** 전공 분야 및 전문 연구 주제 기술
- **주요 프로젝트:** 연구 논문 및 프로젝트 수행 사례
- **논문 발표:** 국제 학술지 및 학회 발표 경력
- **연구 방법론:** 실험 설계, 데이터 분석, 통계 기법 활용
- **협업 경험:** 다학제 팀과의 공동 연구 프로젝트 진행
- **연구 자금:** 연구비 수주 및 관리 경험
- **학위 및 자격:** 관련 전공 학위 및 연구 인증 보유
        """)

    else:
        st.subheader("기타 직무 템플릿")
        st.markdown("해당 직무에 맞는 템플릿을 준비 중입니다.")

def score_system():
    st.header("✅ 점수 시스템 도입")
    st.markdown("AI가 자기소개서 및 면접 답변의 완성도를 평가하여 **점수화** 합니다.<br>강점과 개선점을 시각적으로 확인할 수 있습니다.", unsafe_allow_html=True)
    
    text_input = st.text_area("분석할 텍스트를 입력하세요", height=200, placeholder="예) 제 자기소개서는 ...")
    if st.button("점수 평가하기", key="score"):
        with st.spinner("평가 중..."):
            time.sleep(2)  # 실제 점수 평가 API 연동 시 대체
            score = 85  # 예시 점수
        st.success("평가 완료!")
        st.markdown(f"**총 점수: {score}/100**")
        st.markdown("""
**강점:**  
- 명확한 구성 및 일관된 어휘 사용  

**개선점:**  
- 구체적인 사례 제시 부족  
- 일부 문법적 오류 존재
""")

# --- 메인 함수 및 사이드바 메뉴 ---
def main():
    st.title("AI 자기소개서 & 면접 답변 개선 도구")
    
    # 사이드바 메뉴를 통한 기능 선택
    menu = st.sidebar.radio("메뉴 선택", 
                             ("자기소개서 분석 및 개선", "면접 답변 피드백", "음성 피드백", "이력서 및 지원서 템플릿", "점수 시스템"))
    
    if menu == "자기소개서 분석 및 개선":
        analyze_self_intro()
    elif menu == "면접 답변 피드백":
        interview_feedback()
    elif menu == "음성 피드백":
        audio_feedback()
    elif menu == "이력서 및 지원서 템플릿":
        resume_template()
    elif menu == "점수 시스템":
        score_system()

if __name__ == "__main__":
    main()