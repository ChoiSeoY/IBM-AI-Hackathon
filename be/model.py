import os
import json
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
    Watsonx AI를 이용하여 자기소개서를 분석하고 JSON 형식으로 피드백을 제공하는 함수.
    '''

    prompt_template = f"""
    **🔹 역할: 당신은 전문 자기소개서 평가 AI입니다.**  
    사용자의 자기소개서를 분석하여 **논리적 흐름, 문법 및 맞춤법, 어휘 적절성**을 평가하고 JSON 형식으로 출력하세요.  
    **절대 설명 문장을 포함하지 말고, JSON 데이터만 반환하세요!**

    **🔹 분석 기준**  
    1️⃣ **논리적 흐름 (logic_flow)**: 문장들이 자연스럽게 연결되는지 확인  
    2️⃣ **문법 및 맞춤법 (grammar)**: 문법 및 맞춤법 오류가 있는지 확인  
    3️⃣ **어휘 적절성 (vocabulary)**: 어휘 선택이 적절한지 분석  

    **🔹 반드시 아래 JSON 형식으로만 출력하세요.**
    ```json
    {{
        "logic_flow": "논리적으로 잘 연결된 문장입니다.",
        "grammar": "맞춤법 오류 없음.",
        "vocabulary": "'책임감이 강한 사람' → '책임감이 강한 성격을 지닌 사람' (더 자연스럽게 표현 가능)"
    }}
    ```

    **사용자의 자기소개서:**  
    {user_input}

    **🔹 하나의 JSON만 반환하세요. 설명을 포함하지 마세요.**
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
    print(f"🔎 AI 원본 응답: {response}")  # 디버깅용 출력

    # ✅ JSON 변환 시도
    try:
        response = response.replace("```json", "").replace("```", "").strip()

        # JSON 블록이 두 개 이상이면 마지막 JSON 블록만 추출
        json_blocks = response.split("\n\n")
        if len(json_blocks) > 1:
            response = json_blocks[-1]  # 마지막 JSON 블록 사용

        feedback_json = json.loads(response)  # AI 응답을 JSON 변환
    except json.JSONDecodeError:
        print("⚠ JSON 변환 실패, 원본 응답을 그대로 반환")
        return {"logic_flow": response, "grammar": "JSON 변환 실패", "vocabulary": "JSON 변환 실패"}

    return feedback_json

def qanda_self_intro(user_input):
    '''
    Watsonx AI를 이용하여 면접 답변을 분석하는 함수 (강점, 약점, 개선 사항).
    '''

    prompt_template = f"""
    **🔹 역할: 당신은 전문 면접 코치입니다.**  
    사용자의 면접 답변을 분석하여 **강점, 약점, 개선 사항을 JSON 형식으로 제공하세요.**  
    **반드시 JSON 형식만 출력하고, 추가적인 설명을 포함하지 마세요!**  

    **출력 형식 (반드시 JSON만 반환)**
    ```json
    {{
        "strength": "답변의 강점 분석 결과",
        "weakness": "답변의 약점 분석 결과",
        "improvement": "개선 사항 제안"
    }}
    ```

    **사용자의 면접 답변:**  
    {user_input}

    **반드시 위 JSON 형식만 반환하세요. 설명 문장을 추가하지 마세요!**
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
    print(f"🔎 AI 원본 응답: {response}")  # 디버깅용 출력

    # ✅ JSON 변환 시도
    try:
        response = response.replace("```json", "").replace("```", "").strip()

        # JSON 블록이 두 개 이상이면 마지막 JSON 블록만 추출
        json_blocks = response.split("\n\n")
        if len(json_blocks) > 1:
            response = json_blocks[-1]  # 마지막 JSON 블록 사용

        feedback_json = json.loads(response)  # AI 응답을 JSON 변환
    except json.JSONDecodeError:
        print("⚠ JSON 변환 실패, 원본 응답을 그대로 반환")
        return {"logic_flow": response, "grammar": "JSON 변환 실패", "vocabulary": "JSON 변환 실패"}

    return feedback_json

def mkq_self_intro(user_input, question_count=5):
    '''
    Watsonx AI를 이용하여 지원하는 직종 및 회사에 맞는 면접 예상 질문을 JSON 형식으로 생성하는 함수.
    '''

    print(f"🔎 모델 실행 - 요청된 질문 개수: {question_count}")

    prompt_template = f"""
    **🔹 역할: 당신은 전문 면접관입니다.**  
    당신은 지원자의 **지원 직종 및 회사 정보**를 바탕으로 **실제 면접에서 출제될 가능성이 높은 질문**을 생성하는 역할을 합니다.  
    모든 질문은 **직무 적합성, 핵심 역량 평가, 문제 해결 능력, 팀워크 및 문화 적응력**을 중심으로 작성해야 합니다.  
    또한, 질문 개수를 `{question_count}`개로 제한하여 명확하게 출력하세요.

    **🔹 질문 구성 기준**  
    1️⃣ **직무 기술 평가**: 해당 직무에서 필요한 핵심 기술 및 경험 관련 질문  
    2️⃣ **문제 해결 능력**: 예상되는 업무 문제를 해결하는 능력 평가  
    3️⃣ **팀워크 및 협업**: 팀 내 역할과 협업 스타일을 평가하는 질문  
    4️⃣ **기업 문화 적응력**: 해당 회사의 문화 및 가치관에 적합한지를 평가  
    5️⃣ **자기 계발 및 비전**: 장기적인 성장 방향 및 목표 확인  

    **🔹 지원 정보**  
    지원 직종 및 회사: {user_input}  
    예상 질문 개수: {question_count}

    **🔹 반드시 아래 JSON 형식으로 `{question_count}`개의 질문만 출력하세요.**  
    ```json
    {{
        "questions": [
            "직무와 관련된 가장 중요한 기술은 무엇이며, 이를 활용한 경험을 설명해 주세요.",
            "과거 프로젝트에서 예상치 못한 문제를 어떻게 해결했나요?",
            "팀 내에서 의견 충돌이 발생했을 때 어떻게 해결했나요?",
            "우리 회사의 핵심 가치를 선택하여 본인의 경험과 연결해 설명해 주세요.",
            "5년 후 본인의 커리어 목표는 무엇이며, 이를 위해 어떤 노력을 하고 있나요?"
        ]
    }}
    ```
    **절대로 `{question_count}`개 이상의 질문을 생성하지 마세요!**
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
    print(f"🔎 AI 원본 응답: {response}")  # 디버깅용 출력

    # ✅ JSON 변환 시도
    try:
        # 코드 블록 제거 (AI가 ```json ... ``` 포맷으로 반환하는 경우 방지)
        response = response.replace("```json", "").replace("```", "").strip()

        # JSON 블록이 여러 개 있을 경우 마지막 블록을 사용
        json_blocks = response.split("\n\n")
        for block in json_blocks:
            try:
                parsed_json = json.loads(block)  # JSON 변환 시도
                feedback_json = parsed_json  # 정상적으로 변환되면 저장
            except json.JSONDecodeError:
                continue  # JSON이 아닌 블록은 무시하고 다음 블록 시도

        # 변환 실패 시 기본 오류 메시지 반환
        if not isinstance(feedback_json, dict):
            raise ValueError("JSON 변환 실패: 적절한 JSON 블록을 찾을 수 없음.")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠ JSON 변환 실패: {str(e)}")
        return {"questions": ["❌ JSON 변환 오류 발생"]}

    # ✅ 개수 제한 적용 (AI가 질문 개수를 초과할 경우)
    if "questions" in feedback_json and isinstance(feedback_json["questions"], list):
        print(f"🔎 AI가 반환한 질문 개수: {len(feedback_json['questions'])}")  # AI가 몇 개의 질문을 반환했는지 확인
        print(f"🔎 적용할 질문 개수 제한: {question_count}")  # 사용자 요청 개수 확인
        feedback_json["questions"] = feedback_json["questions"][:question_count]

    return feedback_json

