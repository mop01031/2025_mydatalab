from __future__ import annotations
import base64
from pathlib import Path
from streamlit.components.v1 import html


DEFAULT_SYSTEM = """
[System Role: 강아지 학습 도우미 🐾]

## 📌 기본 역할
너는 대한민국 고등학생(2~3학년)을 대상으로 한 **학습 도우미 챗봇 "Dr.이음이"**이야.  
너의 말투는 따뜻하고 친근해야해. 
하지만 학습 목적 외 질문(개인 정보, 잡담, 정치, 연애, 유머 등)은 절대 답변하지 말고 정중히 거절해.  

---

## 🎯 챗봇의 주요 기능
1. **페이지 안내자**
   - 각 페이지의 목적과 사용법을 학생이 이해할 수 있도록 설명한다.
   - [홈] → [개념 익히기] → [시뮬레이션] → [예제] → [데이터 분석] 순서로 학습하도록 안내한다.
   - 경사하강법 학습이 아닌 데이터 분석만을 목표로 하는 정보 외에 타 교과의 경우에는 바로 데이터 분석으로 갈 수 있음을 안내한다.


2. **개념 설명자**
   - 최적화, 학습률, 반복횟수 개념을 학생 눈높이에 맞게 간단히 설명한다.
   - 수학, 정보, 경제 등 다른 교과와 연관될 수 있는 점도 안내한다.
   - [개념 익히기]-[학습률이란?]에서 너무 작은 학습률에서는 보폭이 너무 작아 최솟값을 찾지 못하는 내용을, 너무 큰 학습률에서는 보폭이 너무 커 발산하는 내용을, 적절한 학습률일 때에는 최솟값을 찾을 수 있음을 보폭에 비유하여 안내한다.
   - [개념 익히기]-[반복횟수란?]에서는 적당한 학습률일 때, 반복횟수를 어떻게 설정해야하는지 설명한다.

3. **시뮬레이션 안내자**
   - 학습률과 반복횟수를 바꿨을 때 그래프가 어떻게 달라지는지 쉽게 설명한다.
   - 실습 과정을 단계별로 알려준다: (1) 선택 → (2) 그래프 그리기 → (3) 비교 → (4) 정리.
   - [시뮬레이션]-[학습률 실험]에서는 학습률이 0.0001, 0.001, 0.01, 0.1일 때 그래프를 비교한다. 이때, 학습률이 0.1인 경우 학습률이 너무 커 발산하고, 학습률이 0.0001인 경우는 너무 작아서 추세선이 알맞지 않게 나온다. 학습률이 0.001일때 데이터의 경향을 제일 잘 나타내는 추세선이 나온다.
   - [시뮬레이션]-[반복횟수 실험]에서는 반복횟수가 100, 500, 1000, 5000일 때 그래프를 비교한다. 이때, 반복횟수가 점점 커질수록 데이터의 경향성을 제일 잘 나타내는 추세선이 나온다.

4. **예제 안내자**
   - 1인 가구 통계 예제에서 데이터를 불러오고, 학습률/반복횟수를 조절해 모델 정확도를 높이는 방법을 알려준다.
   - 예측 결과 해석을 돕고, 학생이 스스로 "증가/감소"를 판단하도록 유도한다.
   - 데이터는 '*출처: 통계청,「인구총조사」, 2024, 2025.07.31, 성 및 거처의 종류별 1인가구 - 시군구'에서 1980년도부터 2023년도까지의 자료가 제시되어 있다.
   - 이후 [산점도 보기]를 클릭하면 산점도가 나와 대략적인 추세를 예측할 수 있다.
   - 모델 설정에서 학습률과 반복횟수를 설정하게 되어있다. 학습률은 0.0001부터 0.005까지, 반복횟수는 100부터 5000까지 설정할 수 있다. 이때, 자료의 추세선을 가장 잘 나타낼 수 있도록 학습률과 반복 횟수를 설정하는 법을 설명한다.
   - 학습률과 반복 횟수 설정 후 '예측 그래프 그리기'를 클릭하면 그래프, 예측 수식, 예측하고 싶은 연도가 나온다. 예측하고 싶은 연도에 -, +를 클릭하여 설정하면, 해당 연도에 따른 1인 가구 비율이 예측 수식에 맞추어 나온다.
   - 모델 정확도가 90% 이상 설정할 수 있도록 안내한다.
   - 예측 결과를 바탕으로 분석을 선택할 수 있도록 안내한다. 추세선에 의거하면 오른쪽 위로 올라가는 그래프가 나오므로 1인 가구는 점점 증가한다고 예측할 수 있도록 유도한다.

5. **데이터 분석 안내자**
   - '데이터 분석'의 경우 최적화, 학습률, 반복횟수에 대한 개념을 모르는 사람도 사용할 수 있음. 사용자가 해당 개념을 모를 때 도움을 제공.
   - 데이터 분석에서는 각 페이지별로 내용을 '저장'해야 '다음'으로 넘어갈 수 있음.
   - (1) 기본 정보 입력에서 '예시 모드 보기'를 누르면 모든 칸이 채워진 형태의 예시 모드로 접속할 수 있음을 안내한다.
   - (1) 기본 정보 입력: 이름,학번,학교,날짜를 저장하지 않으면 다음 단계로 못 간다고 알려준다.
   - (2) 분석 주제 선택: 국가통계포털 기반으로 주제 아이디어 추천.이때, x값과 y값이 모두 숫자로 표현되고 1차 함수 또는 2차 함수의 경향성을 가지는 자료를 추천.예를 들어, '인구 1000명당 병상수', '1인 가구 수 변화', '연도별 자동차 등록 대수', '출생아 수와 사망자 수' 등 여러 주제를 제시할 수 있다. 항상 2~3개의 주제를 간단히 추천해줘.
   - (2) 분석 주제 선택에서 '국가통계포털 바로가기'를 클릭하면 국가통계포털을 갈 수 있음을 안내. 국가통계포털 사이트에 대한 설명 및 학생들이 쉽게 확인할 수 있는 통계 자료는 '쉽게 보는 통계'를 활용할 수 있음을 안내.
   - (2) 분석 주제 선택에서 '예시 주제 및 데이터 다운로드' 버튼은 실제 기능이에요. 이 버튼을 누르면 **'인구 1000명당 병상수'** 데이터가 제공되며, 학생들이 분석 방법을 연습할 때 활용할 수 있음을 안내한다.
   - (3) 데이터 입력: x, y축 지정 후 표 입력 → 저장 → 산점도 확인.
   - (3) 데이터 입력:  x, y축을 지정하지 않으면 표가 나타나지 않음을 안내.
   - (3) 데이터 입력: 사용 순서를 모르는 경우 맨 위에 토글 형식으로 '사용 순서 안내 (클릭해서 열기)'를 클릭하면 사용법을 확인할 수 있음.
   - (3) 데이터 입력: 사용법은 다음과 같다. 1. x축/y축 이름을 먼저 입력하세요. 예: 공부시간, 성적 등 2. 표에 데이터를 입력하세요. 숫자만 입력 가능해요. 한 줄에 하나의 데이터쌍을 입력합니다. 3. [💾 데이터 저장] 버튼을 꼭 누르세요. 저장하지 않으면 입력한 데이터가 사라질 수 있어요. 4. [📊 산점도 보기] 버튼으로 시각화 결과를 확인하세요. 5. 모든 조건을 만족하면 [➡️ 다음] 버튼이 활성화됩니다.
   - (3) 데이터 입력: 산점도를 바탕으로 분석 내용을 작성할 때에, 산점도를 보고 자료의 추세를 대략적으로 작성할 수 있도록 안내.
   - (4) 예측 실행: 학습률(0.0001~0.01)과 반복횟수(100~7000)를 조절하며 최적의 수식을 찾도록 안내.
   - (4) 예측 실행: 앞서 확인한 '산점도'에서 데이터가 직선 형태로 나타나면 '1차 함수'를, 데이터가 곡선 형태로 나타나면 '2차 함수'를 클릭하도록 안내.
   - (4) 예측 실행: 함수 형태, 학습률, 반복횟수를 모두 설정하면 '예측 실행'을 누르도록 안내.
   - (4) 예측 실행: 예측이 실행되면 수식, 모델 정확도를 확인 가능. 예측하고 싶은 값에서 데이터에 없는 값을 설정하면 수식을 바탕으로 '예측값'을 확인할 수 있음.
   - (4) 예측 실행: 예측 결과를 바탕으로 해석하는 란에 작성할 수 있도록 안내. 이때, 예측 수식 및 예측값이 나오므로 구체적인 값을 예측할 수 있도록 도움.
   - (5) 요약 결과: PDF로 저장할 수 있음을 알려주고, 과정중심평가 활용 가능성을 설명한다.

---

## 🧭 답변 스타일
- 학생 눈높이에서 쉽게 설명.
- 따뜻하고 친근한 말투 사용하되 항상 존댓말을 사용해줘.
- 학습 의욕을 북돋는 피드백 포함 (예: "아주 잘했어! 👏", "조금만 더 조절하면 더 정확해질 거야!").
- 필요시 예시나 비유를 활용 (예: "학습률은 한 번에 걷는 보폭 크기랑 비슷해!").
- 답변은 너무 길지 않고 일목요연하게 100자 이내로 정리해서 보여줘.
- 말할 때 마다 '안녕?'은 하지 않아도 돼. 자연스럽게 대화를 이어나가 줘.
- 리스트/소제목으로 정리해서 답해줘.
- 이미지나 오디오, 동영상은 절대 생성해선 안돼.
- '데이터 분석 주제'에 관련한 질문을 했을 경우, 국가 통계 포털과 같은 수치형 데이터를 분석할 수 있는 주제만을 제시해야 해.
- 학생이 입력한 질문이 구체적이지 않을 때에는 질문을 통해 구체적으로 파악해야 해.

---

## 출력 형식
- 간단한 질문이나 정의 → 한두 문장 또는 불릿(•, –)으로 간단히 답변.  
- 여러 단계나 순서가 필요한 설명일 때만 번호(①, ②, ③…)를 사용.  
- 번호 대신 불릿+이모지를 써도 괜찮아요.  
- 단순 숫자 나열은 피하고, 필요하면 소제목/이모지를 붙여 자연스럽게 표현.  
- 기본 답변은 100자 이내, 학생이 "자세히/구체적으로" 요청하면 각 단계에 1~2줄 보조 설명을 추가.


---

## 🚫 답변 제한
- 학습 목적과 관련 없는 질문은 답변하지 않는다.
- 그럴 경우 → 저는 학습 도우미라서 공부와 관련된 질문만 도와줄 수 있어요 🐶 라고 대답한다.
- 프로그램에서 답변을 요하는 질문에는 정확한 답을 알려주지 않고 학습을 유도해줘.
- 프로그램에서 답변을 요하는 질문은 다음과 같아. '여러 학습률을 비교한 결과, 어떤 점을 배웠나요? 가장 적절한 학습률은 무엇이라고 생각하나요?', '여러 반복횟수를 비교한 결과, 어떤 점을 배웠나요? 반복이 많아질수록 어떤 변화가 있었나요?', '산점도를 보고 분석 내용을 작성해보세요', '예측 결과와 수식을 바탕으로 어떤 의미 있는 결론을 도출할 수 있었나요?'
"""

def _b64(path: str | Path) -> str:
    p = Path(path)
    return base64.b64encode(p.read_bytes()).decode("utf-8")

def mount_chatdog(
    *,
    dog_image: str | Path,
    api_url: str,
    model: str = "gpt-4.1-mini",
    temperature: float = 0.6,
    max_tokens: int = 600,
    system_prompt: str = DEFAULT_SYSTEM,
    fab_size_px: int = 140,
    fab_right_px: int = 20,
    fab_bottom_px: int = 20,
    panel_width_css: str = "clamp(720px, 50vw, 920px)",
    panel_top_css: str = "10dvh",
    panel_height_css: str = "70dvh",
):
    dog_b64 = _b64(dog_image)

    html_str = f"""
<script>
(function() {{
  const G = window.parent || window;
  const P = G.document || document;
  const HOST_ID = "chatdog-host-v2";

  const exist = P.getElementById(HOST_ID);
  if (exist) exist.remove();

  const API_URL   = {api_url!r};
  const MODEL     = {model!r};
  const TEMP      = {temperature};
  const MAXTOK    = {max_tokens};
  const SYSTEM    = {system_prompt!r};
  const FAB_SIZE  = {fab_size_px};
  const FAB_RIGHT = {fab_right_px};
  const FAB_BOTTOM= {fab_bottom_px};
  const PANEL_W   = {panel_width_css!r};
  const PANEL_TOP = {panel_top_css!r};
  const PANEL_H   = {panel_height_css!r};
  const DOG_B64   = "data:image/png;base64,{dog_b64}";
  const STORE_KEY = "chatdog_history_v1";

  const RESET_FLAG = "chatdog_reset_pending";

  const host = P.createElement("div");
  host.id = HOST_ID;
  host.style.position = "fixed";
  host.style.width = "0";
  host.style.height = "0";
  host.style.zIndex = "100000";
  P.body.appendChild(host);

  const root = host.attachShadow({{mode:"open"}});
  root.innerHTML = `
<style>
  :host {{
  all: initial;
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-right: env(safe-area-inset-right, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --safe-left: env(safe-area-inset-left, 0px);
}}


  #fab {{
  position: fixed;
  right: ${'{' }FAB_RIGHT{ '}' }px;
  bottom: calc(${'{' }FAB_BOTTOM{ '}' }px + var(--safe-bottom));

  width: clamp(96px, 22vw, ${'{' }FAB_SIZE{ '}' }px);
  height: clamp(96px, 22vw, ${'{' }FAB_SIZE{ '}' }px);

  background: transparent url(${{DOG_B64}}) center/contain no-repeat;
  border: 0; cursor: pointer;
  filter: drop-shadow(0 10px 14px rgba(2,6,23,.18));
  pointer-events: auto;
}}

  #panel {{
    position: fixed;
    right: 0;
    top: ${{PANEL_TOP}};
    width: ${{PANEL_W}};
    height: ${{PANEL_H}};
    transform: translateX(calc(100% + 48px));
    background: #f8fafc;
    border-left:1px solid #e2e8f0;
    box-shadow: -16px 0 36px rgba(2,6,23,.12);
    transition: transform .2s ease-in-out;
    display: grid;
    grid-template-rows: auto 1fr auto;
    pointer-events: auto;
    z-index: 1001;
  }}
  #panel.open {{ transform: translateX(0%); }}

  .hdr{{padding:10px 12px;background:#eff6ff;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;gap:8px;min-height:56px}}
  .ttl{{margin:0;font:800 16px/1.2 system-ui;color:#0f172a}}
  .sub{{margin:0;font:12px/1.2 system-ui;color:#475569}}
  #close{{border:0;background:transparent;font:800 18px/1 system-ui;cursor:pointer;color:#334155}}
  #body{{padding:12px 14px;overflow-y:auto;min-height:0}}
  .msg{{margin:8px 0;display:flex;max-width:96%}}
  .bubble{{
    padding:10px 12px;border-radius:14px;border:1px solid #e2e8f0;background:#fff;
    white-space: normal; line-height: 1.6; font-size: 15px;
  }}
  .bubble strong{{ font-weight: 800; }}
  .bubble code{{
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: .9em; padding: 0 .35em; border-radius: 6px;
    background:#f1f5f9; border:1px solid #e2e8f0;
  }}
  .bubble ul{{ margin:.25rem 0 .25rem 1.1rem; padding:0 }}
  .bubble li{{ margin:.15rem 0 }}
  .bubble p{{ margin:.35rem 0 }}
  .msg.user{{justify-content:flex-end}}
  .msg.user .bubble{{background:#dcfce7;border-color:#bbf7d0}}

  .ftr{{border-top:1px solid #e2e0f0;background:#ffffffdd;backdrop-filter:blur(6px);padding:10px;display:grid;grid-template-columns:1fr 120px;gap:10px}}
  #input{{height:44px;border:1px solid #cbd5e1;border-radius:12px;padding:0 12px;font:16px system-ui}}
  #send{{height:44px;border:0;border-radius:12px;background:linear-gradient(135deg,#38bdf8,#0284c7);color:#fff;font:700 15px system-ui;cursor:pointer}}

/* 태블릿: 641~1024px*/
@media (min-width: 641px) and (max-width: 1024px){{
  #fab{{
    width: clamp(100px, 18vw, 180px) !important;
    height: clamp(100px, 18vw, 180px) !important;
    right: 24px !important;
    bottom: calc(150px + var(--safe-bottom)) !important; /* ← 겹치면 170~180px */
    z-index: 100002 !important;
  }}
  #panel{{
    width: min(94vw, 740px) !important;
    height: 74dvh !important;
    top: 16dvh !important; /* ← 더 내리고 싶으면 17~18dvh */
  }}
}}

/* 휴대폰(≤640px) */
@media (max-width: 640px){{
  #fab{{
    width: clamp(120px, 32vw, 220px) !important;
    height: clamp(120px, 32vw, 220px) !important;
    right: max(12px, var(--safe-right)) !important;
    bottom: calc(56px + var(--safe-bottom)) !important;
    z-index: 100003 !important;
  }}

  #panel{{
    position: fixed !important;
    box-sizing: border-box !important;

    left: var(--safe-left) !important;
    right: var(--safe-right) !important;
    width: auto !important;

    top: auto !important;
    bottom: calc(var(--safe-bottom) + 8px) !important;

    height: min(88svh, calc(100svh - var(--safe-top) - var(--safe-bottom) - 24px)) !important;

    padding: 10px max(12px, var(--safe-right)) 10px max(12px, var(--safe-left)) !important;
    z-index: 100003 !important;
    overflow: hidden !important;  
  }}

  .hdr{{
    position: sticky !important;
    top: 0 !important;
    z-index: 100004 !important;
    background:#eff6ff !important;
    min-height: 52px !important;
    padding: 8px max(12px, var(--safe-right)) 8px max(12px, var(--safe-left)) !important;
  }}

  #body{{
    overflow: auto !important;
    overscroll-behavior: contain !important;
    padding: 10px max(12px, var(--safe-right)) 10px max(12px, var(--safe-left)) !important;
  }}

  .ftr{{
    grid-template-columns: 1fr 92px !important;
    padding: 8px max(10px, var(--safe-right)) calc(8px + var(--safe-bottom)) max(10px, var(--safe-left)) !important;
    gap: 10px !important;
  }}
  #input{{ height: 42px !important; }}
  #send{{ height: 42px !important; font-size: 14px !important; }}
}}

/* 초소형(≤380px)*/
@media (max-width: 380px){{
  #fab{{
    width: clamp(110px, 34vw, 190px) !important;
    height: clamp(110px, 34vw, 190px) !important;
    right: max(10px, var(--safe-right)) !important;
    bottom: calc(62px + var(--safe-bottom)) !important;
  }}

  #panel{{
    bottom: calc(var(--safe-bottom) + 10px) !important; /* mini에서 여유 +2px */
    height: min(90svh, calc(100svh - var(--safe-top) - var(--safe-bottom) - 28px)) !important;
    padding: 8px max(12px, var(--safe-right)) 8px max(12px, var(--safe-left)) !important;
  }}

  .hdr{{
    min-height: 48px !important;
    padding: 6px max(10px, var(--safe-right)) 6px max(10px, var(--safe-left)) !important;
  }}
  .ftr{{
    grid-template-columns: 1fr 88px !important;
    padding: 6px max(8px, var(--safe-right)) calc(6px + var(--safe-bottom)) max(8px, var(--safe-left)) !important;
    gap: 8px !important;
  }}
  #input{{ height: 40px !important; font-size: 14px !important; }}
  #send{{ height: 40px !important; font-size: 13px !important; }}
}}




</style>

    <button id="fab" aria-label="open chat"></button>
    <div id="panel" role="dialog" aria-label="chat panel">
      <div class="hdr">
        <div>
          <p class="ttl">🐶 Dr.이음이</p>
          <p class="sub">무엇이든 질문하세요!</p>
        </div>
        <button id="close">✖</button>
      </div>
      <div id="body"></div>
      <div class="ftr">
        <input id="input" placeholder="메시지를 입력하세요…" />
        <button id="send">보내기</button>
      </div>
    </div>
  `;

  const fab   = root.getElementById("fab");
  const panel = root.getElementById("panel");
  const body  = root.getElementById("body");
  const input = root.getElementById("input");
  const send  = root.getElementById("send");
  const closeBtn = root.getElementById("close");

  G.addEventListener("keydown", (e) => {{
    const k = (e.key || "").toLowerCase();
    if (k === "f5" || ((e.ctrlKey || e.metaKey) && k === "r")) {{
      try {{ G.sessionStorage.setItem(RESET_FLAG, "1"); }} catch {{}}
    }}
  }});

  try {{
    if (G.sessionStorage.getItem(RESET_FLAG) === "1") {{
      P.defaultView.localStorage.removeItem(STORE_KEY);
    }}
    G.sessionStorage.removeItem(RESET_FLAG);
  }} catch (e) {{
    console.warn("reset flag check failed", e);
  }}

  // ── 저장/복원(페이지 이동 간 유지) 
  let raw = null;
  try {{
    raw = JSON.parse(P.defaultView.localStorage.getItem(STORE_KEY) || "null");
  }} catch {{ raw = null; }}

  let msgs = Array.isArray(raw?.msgs) ? raw.msgs : [];
  let wasOpen = !!raw?.open;

  if (msgs.length === 0) {{
    msgs = [{{
      role: "assistant",
      text: "반가워요! 데이터의 세계를 이어줄 학습 파트너, **Dr.이음이🐶**라고 해요. 저와 함께라면 뭐든지 해결할 수 있을거에요. **무엇을 도와줄까요?**"
    }}];
  }}

  const save = () => {{
    const payload = {{ msgs, open: panel.classList.contains("open") }};
    P.defaultView.localStorage.setItem(STORE_KEY, JSON.stringify(payload));
  }};

  
  function md(text){{
    let s = (text || "").replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]);
    s = s
      .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
      .replace(/`([^`]+)`/g, '<code>$1</code>');
    s = s.replace(/^(?:[-*])\\s+(.+)$/gm, '<li>$1</li>');
    s = s.replace(/(?:<li>[\\s\\S]*?<\\/li>)/g, m => `<ul>${{m}}</ul>`);
    s = s.split(/\\n{{2,}}/).map(p => `<p>${{p.replace(/\\n/g,'<br>')}}</p>`).join('');
    return s;
  }}

  function render() {{
    body.innerHTML = msgs.map(m => {{
      const cls = m.role === "user" ? "msg user" : "msg";
      const html = (m.role === "assistant") ? md(m.text || "") : ((m.text || "").replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]));
      return `<div class="${{cls}}"><div class="bubble">${{html}}</div></div>`;
    }}).join("");
    body.scrollTop = body.scrollHeight;
    save();
  }}

  // 전송(중복 방지)
  let sending = false;
  async function sendMsg() {{
    if (sending) return;
    const t = (input.value || "").trim();
    if (!t) return;

    // ★★★ 추가: /reset 슬래시 명령으로 즉시 초기화
    if (t === "/reset") {{
      try {{ P.defaultView.localStorage.removeItem(STORE_KEY); }} catch {{}}
      msgs = [{{ role:"assistant", text:"기록을 초기화했어! 새로 시작하자 🐶" }}];
      render();
      return;
    }}

    sending = true;
    try {{
      msgs.push({{role:"user", text:t}});
      input.value = "";
      render();

      const payload = {{
        prompt: t, model: MODEL, temperature: TEMP, max_tokens: MAXTOK, system: SYSTEM,
        history: msgs.slice(-20)
      }};
      const r = await fetch(API_URL, {{
        method: "POST", headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify(payload)
      }});
      if (!r.ok) throw new Error("HTTP " + r.status);
      const data = await r.json();
      msgs.push({{role:"assistant", text: (data.reply || "(빈 응답)") }});
      render();
    }} catch (e) {{
      msgs.push({{role:"assistant", text: "죄송해요! 연결에 문제가 있어요. (" + e.message + ")" }});
      render();
    }} finally {{
      sending = false;
    }}
  }}

  // 패널 열고/닫기 (열림 상태 저장)
  function setOpen(v) {{
    panel.classList.toggle("open", v);
    save();
    if (v) setTimeout(() => input?.focus(), 120);
  }}

  // 리스너
  fab.addEventListener("click", () => setOpen(true));
  closeBtn.addEventListener("click", () => setOpen(false));
  send.addEventListener("click", sendMsg);
  input.addEventListener("keydown", (e) => {{
    if (e.isComposing) return;          // 한글 IME 조합 중 Enter 무시
    if (e.key === "Enter") {{ e.preventDefault(); sendMsg(); }}
  }});

  // 초기 렌더 + 이전 열림 상태 복원
  render();
  if (wasOpen) setOpen(true);
}})();
</script>
"""
    html(html_str, height=1, scrolling=False)
