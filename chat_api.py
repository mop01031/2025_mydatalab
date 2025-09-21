from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, pathlib

from openai import OpenAI

def _load_api_key():
    for k in ("OPENAI_API_KEY",):
        if os.getenv(k):
            return os.getenv(k)

    secrets = pathlib.Path(".streamlit/secrets.toml")
    if secrets.exists():
        try:
            import tomllib as tomli  
        except ModuleNotFoundError:
            import tomli  
        data = tomli.loads(secrets.read_text(encoding="utf-8"))
        for k in ("openai_api_key", "OPENAI_API_KEY"):
            if data.get(k):
                return data[k]

    raise RuntimeError("OpenAI API 키가 설정되지 않았습니다. 환경변수 OPENAI_API_KEY 또는 .streamlit/secrets.toml 을 확인하세요.")

API_KEY = _load_api_key()

BASE_URL = os.getenv("OPENAI_BASE_URL", None)
client = OpenAI(api_key=API_KEY) if not BASE_URL else OpenAI(api_key=API_KEY, base_url=BASE_URL)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://2025mydatalab.streamlit.app"],
    allow_credentials=False,  
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"  
    temperature: float = 0.6
    max_tokens: int = 600
    system: str | None = None
    history: list[dict] | None = None 

class ChatResponse(BaseModel):
    reply: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/chatdog", response_model=ChatResponse)
def chatdog(req: ChatRequest):
    system_instruction = req.system or "You are a helpful assistant."

    messages = [{"role": "system", "content": system_instruction}]

    if req.history:
        for m in req.history:
            role = m.get("role", "user")
            text = (m.get("text") or m.get("content") or "").strip()
            if text:
                messages.append({"role": role, "content": text})

    if req.prompt:
        messages.append({"role": "user", "content": req.prompt})

    completion = client.chat.completions.create(
        model=req.model,
        messages=messages,
        temperature=req.temperature,
        max_tokens=int(req.max_tokens),
    )

    text = (completion.choices[0].message.content or "").strip()
    return {"reply": text or "(빈 응답)"}
