# chat_api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, pathlib, sys

import google.generativeai as genai

# ---- API 키 로딩: 환경변수 우선, 없으면 .streamlit/secrets.toml에서 읽기 ----
def _load_api_key():
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.getenv(k):
            return os.getenv(k)
    # secrets.toml에서 읽기 (로컬 편의)
    secrets = pathlib.Path(".streamlit/secrets.toml")
    if secrets.exists():
        try:
            import tomllib as tomli  # py>=3.11
        except ModuleNotFoundError:
            import tomli  # py<3.11
        data = tomli.loads(secrets.read_text(encoding="utf-8"))
        for k in ("gemini_api_key","google_api_key","GEMINI_API_KEY","GOOGLE_API_KEY"):
            if data.get(k):
                return data[k]
    raise RuntimeError("Gemini API 키가 설정되지 않았습니다.")

API_KEY = _load_api_key()
genai.configure(api_key=API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    model: str = "gemini-1.5-flash"
    temperature: float = 0.6
    max_tokens: int = 600
    system: str | None = None
    history: list[dict] | None = None  # [{role:"user"/"assistant", text:"..."}]

class ChatResponse(BaseModel):
    reply: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/chatdog", response_model=ChatResponse)
def chatdog(req: ChatRequest):
    # 시스템 프롬프트
    system_instruction = req.system or "You are a helpful assistant."

    model = genai.GenerativeModel(
        model_name=req.model,
        system_instruction=system_instruction,
    )

    # 히스토리가 있으면 순서대로, 없으면 현재 프롬프트만
    parts: list[str] = []
    if req.history:
        for m in req.history:
            t = (m.get("text") or m.get("content") or "").strip()
            if t:
                parts.append(t)
    if req.prompt:
        parts.append(req.prompt)

    resp = model.generate_content(
        parts,
        generation_config={
            "temperature": req.temperature,
            "max_output_tokens": int(req.max_tokens),
        },
    )
    text = (getattr(resp, "text", "") or "").strip()
    return {"reply": text or "(빈 응답)"}
