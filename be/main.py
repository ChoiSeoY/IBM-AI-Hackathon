from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 초기화
app = FastAPI()

# Watsonx AI API 인증 정보 설정
API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
IBM_URL = os.getenv("URL")

credentials = {
    "url": IBM_URL,
    "apikey": API_KEY
}

MISTRAL_LARGE = "mistralai/mistral-large"

# 요청 데이터 모델
class SelfIntroRequest(BaseModel):
    user_text: str

# Watsonx AI 분석 함수 (model.py에서 가져오기)
from model import analyze_self_intro, qanda_self_intro

# API 엔드포인트 (POST 요청) -자소서
@app.post("/analyze")
async def analyze_intro(request: SelfIntroRequest):
    feedback = analyze_self_intro(request.user_text)
    return {"feedback": feedback}

# API 엔드포인트 (POST 요청) -면접접
@app.post("/qanda")
async def qanda_intro(request: SelfIntroRequest):
    feedback = qanda_self_intro(request.user_text)
    return {"feedback": feedback}

# 서버 상태 확인 엔드포인트
@app.get("/health")
async def health_check():
    return {"status": "running"}
