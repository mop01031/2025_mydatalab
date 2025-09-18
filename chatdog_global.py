# chatdog_global.py
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

2. **개념 설명자**
   - 최적화, 학습률, 반복횟수 개념을 학생 눈높이에 맞게 간단히 설명한다.
   - 수학, 정보, 경제 등 다른 교과와 연관될 수 있는 점도 안내한다.

3. **시뮬레이션 안내자**
   - 학습률과 반복횟수를 바꿨을 때 그래프가 어떻게 달라지는지 쉽게 설명한다.
   - 실습 과정을 단계별로 알려준다: (1) 선택 → (2) 그래프 그리기 → (3) 비교 → (4) 정리.

4. **예제 안내자**
   - 1인 가구 통계 예제에서 데이터를 불러오고, 학습률/반복횟수를 조절해 모델 정확도를 높이는 방법을 알려준다.
   - 예측 결과 해석을 돕고, 학생이 스스로 "증가/감소"를 판단하도록 유도한다.

5. **데이터 분석 안내자**
   - (1) 기본 정보 입력: 이름,학번,학교,날짜를 저장하지 않으면 다음 단계로 못 간다고 알려준다.
   - (2) 분석 주제 선택: 국가통계포털 기반으로 주제 아이디어 추천.
   - (3) 데이터 입력: x, y축 지정 후 표 입력 → 저장 → 산점도 확인.
   - (4) 예측 실행: 학습률과 반복횟수를 조절하며 최적의 수식을 찾도록 안내.
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
---

## 🚫 답변 제한
- 학습 목적과 관련 없는 질문은 답변하지 않는다.
- 그럴 경우 → 저는 학습 도우미라서 공부와 관련된 질문만 도와줄 수 있어요 🐶 라고 대답한다.
"""

def _b64(path: str | Path) -> str:
    p = Path(path)
    return base64.b64encode(p.read_bytes()).decode("utf-8")

def mount_chatdog(
    *,
    dog_image: str | Path,
    api_url: str,
    model: str = "gpt-3.5-turbo",
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
    """우하단 강아지 버튼 + 오른쪽 패널을 부모 문서(Shadow DOM)로 삽입"""
    dog_b64 = _b64(dog_image)

    html_str = f"""
<script>
(function() {{
  const G = window.parent || window;
  const P = G.document || document;
  const HOST_ID = "chatdog-host-v2";

  // 항상 새로 만들되, 이전 것이 있다면 제거(리스너 꼬임 방지)
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

  // ★★★ 추가: 강제 새로고침 감지용 세션 플래그
  const RESET_FLAG = "chatdog_reset_pending";

  // 호스트(0x0) + Shadow DOM
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
    --safe-bottom: env(safe-area-inset-bottom, 0px); 
  }}

  #fab {{
    position: fixed;
    right: ${'{' }FAB_RIGHT{ '}' }px;
    bottom: calc(${'{' }FAB_BOTTOM{ '}' }px + var(--safe-bottom));
    width: ${'{' }FAB_SIZE{ '}' }px;
    height: ${'{' }FAB_SIZE{ '}' }px;
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

  /* 반응형 오버라이드 */
  @media (max-width: 1024px){{
    #fab{{ width:100px; height:100px; }}
    #panel{{ width:min(94vw,740px); height:72dvh; top:7dvh; }}
  }}

  @media (max-width: 640px){{
    #fab{{ width:88px; height:88px; right:12px; }}
    #panel{{ width:min(94vw,560px); height:74dvh; top:6dvh; }}
    .ftr{{ grid-template-columns: 1fr 104px; }}
  }}

  @media (max-width: 380px){{
    #fab{{ width:78px; height:78px; right:10px; }}
    #panel{{ width:96vw; height:76dvh; top:5dvh; }}
    .ftr{{ grid-template-columns: 1fr 96px; }}
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

  // ★★★ 추가: Ctrl/⌘+R 또는 F5 입력 시, 다음 로드에서 리셋하도록 세션 플래그 설정
  G.addEventListener("keydown", (e) => {{
    const k = (e.key || "").toLowerCase();
    if (k === "f5" || ((e.ctrlKey || e.metaKey) && k === "r")) {{
      try {{ G.sessionStorage.setItem(RESET_FLAG, "1"); }} catch {{}}
    }}
  }});

  // ★★★ 추가: 로드 시 플래그 확인 → 한 번만 기록 초기화
  try {{
    if (G.sessionStorage.getItem(RESET_FLAG) === "1") {{
      P.defaultView.localStorage.removeItem(STORE_KEY);
    }}
    G.sessionStorage.removeItem(RESET_FLAG);
  }} catch (e) {{
    console.warn("reset flag check failed", e);
  }}

  // ── 저장/복원(페이지 이동 간 유지) ─────────────────────────────────
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

  // ── Markdown 렌더러 ──────────────────────────────────────────────
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
    # 부모에 붙이므로 iframe 자체 높이는 1로 충분
    html(html_str, height=1, scrolling=False)
