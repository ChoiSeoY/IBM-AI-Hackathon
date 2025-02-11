import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# 환경 변수 로드
load_dotenv()

# API 정보 가져오기
API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
IBM_URL = os.getenv("URL")

credentials = {
    "url": IBM_URL,
    "apikey": API_KEY
}

MISTRAL_LARGE = "mistralai/mistral-large"

# Watsonx AI 요청 함수 정의
def analyze_self_intro(user_input):
    '''
    Watsonx AI를 이용하여 자기소개서의 논리적 흐름, 문법, 어휘 적절성을 분석하고 구체적인 피드백을 제공하는 함수.
    '''

    prompt_template = f"""
    **자기소개서 분석 기준**  
    1️⃣ 논리적 흐름  
    2️⃣ 문법 및 맞춤법  
    3️⃣ 어휘 적절성  

    **사용자의 자기소개서:**  
    {user_input}

    **출력 형식 예시:**  
    ✅ 논리적 흐름: 문장이 자연스럽게 연결됨.  
    ✅ 문법 및 맞춤법: 맞춤법 오류 없음.  
    ✅ 어휘 적절성: "책임감이 강하고 성실한 사람입니다." → "책임감이 강하고 성실한 성격을 가지고 있습니다."  

    **위와 동일한 형식으로 출력하세요.**
    """

    model_params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MIN_NEW_TOKENS: 50,
        GenParams.MAX_NEW_TOKENS: 1000,
        GenParams.RANDOM_SEED: 42,
        GenParams.TEMPERATURE: 0.7,
        GenParams.REPETITION_PENALTY: 1.05,
    }

    model = Model(
        model_id=MISTRAL_LARGE,
        params=model_params,
        credentials=credentials,
        project_id=PROJECT_ID
    )

    response = model.generate_text(prompt=prompt_template)
    return response.strip().replace("\n    ", "\n")

def qanda_self_intro(user_input):
    '''
    Watsonx AI를 이용하여 자기소개서의 논리적 흐름, 문법, 어휘 적절성을 분석하고 구체적인 피드백을 제공하는 함수.
    '''

    prompt_template = f"""
    **🔹 역할: 당신은 전문 면접 코치입니다.**  
    당신은 전문 면접 코치로서, 사용자가 제공한 면접 답변을 분석하여 **강점, 단점, 그리고 개선 사항을 논리적으로 제안하는 역할**을 한다.  
    **논리적이고 체계적인 구조를 유지하며**, 반드시 줄글 형식으로 작성하라.

    **🔹 분석 기준**  
1️⃣ **강점**: 답변에서 잘 표현된 부분을 짚어주세요.  
2️⃣ **약점**: 다소 모호하거나 개선이 필요한 부분을 지적하세요.  
3️⃣ **개선 방안**: 더 나은 답변이 될 수 있도록 구체적인 수정 예시를 제안하세요.

    **🔹 질문 분석**  
    사용자가 제공한 면접 답변에서 **핵심 키워드**를 식별하고, 반드시 해당 키워드와 연관된 분석을 수행하라.  

    **사용자의 면접 답변:**  
    {user_input}

    **🔹 출력 형식 예시**  
    - **강점 분석:** 답변이 논리적으로 정리되어 있으며, 직무 관련 역량을 잘 드러냅니다.
    - **약점 분석:** 경험 설명이 다소 일반적이어서 구체적인 사례 추가가 필요합니다. 
    - **개선 사항:** "저는 문제 해결력이 뛰어납니다" → "저는 [특정 상황]에서 [구체적 행동]을 통해 문제를 해결한 경험이 있습니다."
    **위와 동일한 형식으로 분석하여 답변하라.**
    """

    model_params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MIN_NEW_TOKENS: 50,
        GenParams.MAX_NEW_TOKENS: 1000,
        GenParams.RANDOM_SEED: 42,
        GenParams.TEMPERATURE: 0.5,
        GenParams.REPETITION_PENALTY: 1.1,
    }

    model = Model(
        model_id=MISTRAL_LARGE,
        params=model_params,
        credentials=credentials,
        project_id=PROJECT_ID
    )

    response = model.generate_text(prompt=prompt_template)
    print(f"🔎 AI 응답: {response}")

    return response.strip().replace("\n    ", "\n")
