import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# 1. 환경 변수 로드
load_dotenv()

# 2. API 정보 가져오기
try:
    apikey = os.environ["API_KEY"]
except KeyError:
    apikey = input("Please enter your API KEY (hit enter): ")

try:
    project_id = os.environ["PROJECT_ID"]
except KeyError:
    project_id = input("Please enter your project_id (hit enter): ")

try:
    url = os.environ["URL"]
except KeyError:
    url = input("Please enter your URL (hit enter): ")

# 3. Watsonx AI API 인증 정보 설정
credentials = {
    "url": url,
    "apikey": apikey
}

MISTRAL_LARGE = "mistralai/mistral-large"

# 4. Watsonx AI 요청 함수 정의
def analyze_self_intro(user_input,
                       model_name=MISTRAL_LARGE,
                       decoding_method="greedy",
                       max_new_tokens=1000, 
                       min_new_tokens=50,
                       temperature=0.7,
                       repetition_penalty=1.05):
    '''
    Watsonx AI를 이용하여 자기소개서의 논리적 흐름, 문법, 어휘 적절성을 분석하고 구체적인 피드백을 제공하는 함수.
    '''

    # ✅ 개행을 강제하도록 명확한 출력 형식 추가
    prompt_template = f"""
    당신은 전문적인 작문 평가자입니다.  
    아래 자기소개서를 분석하고, 다음 3가지 기준을 바탕으로 **구체적인 피드백을 제공하세요.**  
    **출력 형식에서 반드시 줄바꿈(\\n)을 유지하며, 한 줄에 하나의 문장만 출력하도록 하세요.**  

    **1. 논리적 흐름 (Logical Coherence)**  
    - 문장이 자연스럽게 연결되는가?  
    - 전체적인 구조가 명확한가? (두괄식, 결론 정리 등)  
    - 주제가 일관되게 유지되는가?  
    - ✅ 논리적 흐름 피드백: (자기소개서에서 개선할 부분과 예시 제공)  

    **2. 문법 및 맞춤법 (Grammar & Spelling)**  
    - 맞춤법 오류가 있는가?  
    - 문장이 어색하거나 비문이 포함되어 있는가?  
    - ✅ 문법 및 맞춤법 피드백: (어색한 표현과 대체 문장 예시 제공)  

    **3. 어휘 적절성 (Word Choice)**  
    - 더 나은 표현이 가능한 단어가 있는가?  
    - 어휘 선택이 적절한가?  
    - 직무나 맥락에 맞는 단어를 사용하고 있는가?  
    - ✅ 어휘 적절성 피드백: (더 자연스러운 단어 또는 문장 수정 예시 제공)  

    **사용자의 자기소개서:**  
    
{user_input}


    **📌 피드백 형식 예시:**  
    ✅ 논리적 흐름: 문장이 자연스럽게 연결되며, 전체적인 구조가 명확하게 제시됨.  
    ✅ 문법 및 맞춤법: 맞춤법 오류 없음. "항상 새로운 도전에 긍정적으로 임하며" 대신 "항상 새로운 도전에 긍정적으로 임합니다."와 같은 표현이 더 자연스러움.  
    ✅ 어휘 적절성: "책임감이 강하고 성실한 사람입니다." 대신 "책임감이 강하고 성실한 성격을 가지고 있습니다."와 같은 표현이 더 자연스러움.  

    **출력 형식을 위 예제와 동일하게 유지하며, 한 줄에 하나의 문장만 출력하세요.**  
    """

    # Watsonx AI 모델 설정
    model_params = {
        GenParams.DECODING_METHOD: decoding_method,
        GenParams.MIN_NEW_TOKENS: min_new_tokens,
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.RANDOM_SEED: 42,
        GenParams.TEMPERATURE: temperature,
        GenParams.REPETITION_PENALTY: repetition_penalty,
    }

    # 모델 실행
    model = Model(
        model_id=model_name,
        params=model_params,
        credentials=credentials,
        project_id=project_id
    )

    response = model.generate_text(prompt=prompt_template)

    # ✅ 개행을 유지하고 불필요한 공백 제거
    formatted_response = response.strip().replace("\n    ", "\n")

    return formatted_response


# 5. 사용자 입력 받기
user_self_intro = """
저는 되돌아보면 열심히 살지 않았던 적이 거의 없었던 것 같습니다. 매사에 최선을 다하며, 대학교에서는 많은 프로젝트도 참가했습니다.
이러한 경험들이 저의 직무에 도움이 분명히 될 것이라 확신하고, 회사에 도움이 되는 사람이 될 수 있으리라 확신합니다.
"""

# 6. Watsonx AI에 자기소개서 분석 요청
evaluation = analyze_self_intro(user_self_intro)

# 7. 결과 출력
print("\n✨ 자기소개서 평가 결과 ✨\n")
print(evaluation)