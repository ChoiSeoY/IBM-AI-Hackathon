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
