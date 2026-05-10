"""v2/1강 HTML 슬라이드 48장 + index 생성기.
script.md의 [데모: NN-xxx.html] 마커와 1:1 매칭.
army/1강/slides 디자인 시스템 (다크 #0a0f1a, 보라→하늘 그라디언트, Noto Sans KR) 차용.
"""
from pathlib import Path

OUT = Path(__file__).parent
TOTAL = 48

# ======================= 공통 CSS =======================
COMMON_CSS = """* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0a0f1a;
  font-family: 'Noto Sans KR', sans-serif;
  color: #e6edf3;
  min-height: 100vh;
  display: flex; justify-content: center; align-items: center;
  padding-bottom: 50px;
}
.container {
  width: 1280px; padding: 44px 80px;
  display: flex; flex-direction: column; align-items: center;
}
.eyebrow {
  font-size: 14px; font-weight: 700; letter-spacing: 4px;
  color: #a78bfa; margin-bottom: 14px; text-transform: uppercase;
}
.title {
  font-size: 44px; font-weight: 900;
  background: linear-gradient(135deg, #7c3aed, #38bdf8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  text-align: center; margin-bottom: 18px; line-height: 1.3;
}
.subtitle { font-size: 17px; color: #8b949e; text-align: center; margin-bottom: 32px; line-height: 1.6; }
.note { text-align: center; font-size: 15px; color: #8b949e; margin-top: 18px; line-height: 1.6; }
.note strong { color: #c9d1d9; }
.callout {
  margin-top: 22px; padding: 14px 24px;
  background: rgba(124, 58, 237, 0.08); border: 1px solid rgba(124, 58, 237, 0.3);
  border-radius: 10px; font-size: 15px; color: #c9d1d9; text-align: center;
  max-width: 900px;
}
.callout strong { color: #a78bfa; }

/* 코드 박스 */
.code-box {
  background: rgba(22, 27, 40, 0.85);
  border: 1px solid rgba(124, 58, 237, 0.25);
  border-radius: 12px;
  padding: 20px 28px;
  font-family: 'Courier New', monospace;
  font-size: 14px; color: #c9d1d9;
  white-space: pre; line-height: 1.7;
  max-width: 1080px; width: 100%;
  overflow-x: auto;
}
.code-box .hl { color: #a78bfa; font-weight: 700; }
.code-box .dim { color: #6e7681; }
.code-box .ok { color: #34d399; }
.code-box .bad { color: #ef4444; }

/* 프롬프트 박스 (함께 입력) */
.prompt-box {
  background: rgba(22, 27, 40, 0.8);
  border: 1px solid rgba(124, 58, 237, 0.3);
  border-radius: 12px;
  padding: 16px 24px;
  font-family: 'Courier New', monospace;
  font-size: 15px; color: #c9d1d9;
  margin-bottom: 28px; max-width: 900px; width: 100%;
}
.prompt-tag {
  display: inline-block; font-family: 'Noto Sans KR', sans-serif;
  font-size: 11px; font-weight: 700; letter-spacing: 1px;
  color: #a78bfa; background: rgba(124, 58, 237, 0.15);
  padding: 3px 10px; border-radius: 4px; margin-bottom: 8px;
}
.prompt-arrow { color: #7c3aed; }

/* 2-col 비교 */
.compare-2col {
  display: grid; grid-template-columns: 1fr auto 1fr; gap: 18px;
  align-items: stretch; width: 100%; max-width: 1100px;
}
.comp-side { border-radius: 14px; padding: 22px 26px; display: flex; flex-direction: column; gap: 10px; }
.comp-old { background: rgba(139, 148, 158, 0.06); border: 1px solid rgba(139, 148, 158, 0.18); }
.comp-new { background: rgba(124, 58, 237, 0.08); border: 1px solid rgba(124, 58, 237, 0.3); }
.comp-label { font-size: 12px; font-weight: 700; letter-spacing: 1px; }
.comp-old .comp-label { color: #8b949e; }
.comp-new .comp-label { color: #a78bfa; }
.comp-body { font-size: 14px; color: #c9d1d9; line-height: 1.7; }
.comp-body code { font-family: 'Courier New', monospace; font-size: 13px; color: #e6edf3; background: rgba(0,0,0,0.25); padding: 1px 6px; border-radius: 3px; }
.comp-arrow { font-size: 26px; color: #7c3aed; align-self: center; }

/* 카드 그리드 (2x2 / 3개 / 4개) */
.card-grid {
  display: grid; gap: 16px;
  width: 100%; max-width: 1100px;
}
.card-grid-2 { grid-template-columns: 1fr 1fr; }
.card-grid-3 { grid-template-columns: 1fr 1fr 1fr; }
.card-grid-4 { grid-template-columns: 1fr 1fr 1fr 1fr; }
.card {
  background: rgba(139, 148, 158, 0.04); border: 1px solid rgba(139, 148, 158, 0.15);
  border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 8px;
}
.card.accent { background: rgba(124, 58, 237, 0.06); border-color: rgba(124, 58, 237, 0.3); }
.card .card-num { font-size: 22px; font-weight: 900; color: #a78bfa; }
.card .card-title { font-size: 16px; font-weight: 700; color: #e6edf3; }
.card .card-body { font-size: 13px; color: #8b949e; line-height: 1.6; }

/* 동심원 */
.three-circles {
  position: relative; width: 520px; height: 380px;
  display: flex; align-items: center; justify-content: center;
}
.circle {
  position: absolute; border-radius: 50%; border: 2px solid;
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-family: 'Noto Sans KR', sans-serif;
}
.circle-outer { width: 380px; height: 380px; border-color: #38bdf8; background: rgba(56, 189, 248, 0.04); color: #38bdf8; font-size: 18px; align-items: flex-start; padding-top: 18px; }
.circle-mid { width: 240px; height: 240px; border-color: #a78bfa; background: rgba(167, 139, 250, 0.06); color: #a78bfa; font-size: 16px; align-items: flex-start; padding-top: 16px; }
.circle-inner { width: 120px; height: 120px; border-color: #ec4899; background: rgba(236, 72, 153, 0.10); color: #f9a8d4; font-size: 14px; }

/* 타임라인 */
.timeline { width: 100%; max-width: 820px; padding-left: 12px; }
.t-row { display: flex; gap: 24px; padding: 14px 0 14px 28px; border-left: 3px solid rgba(124, 58, 237, 0.4); position: relative; }
.t-row::before { content: ''; position: absolute; left: -9px; top: 22px; width: 14px; height: 14px; border-radius: 50%; background: #7c3aed; box-shadow: 0 0 0 4px rgba(124,58,237,0.2); }
.t-row.accent { border-color: rgba(56, 189, 248, 0.6); }
.t-row.accent::before { background: #38bdf8; box-shadow: 0 0 0 4px rgba(56,189,248,0.2); }
.t-date { color: #a78bfa; font-weight: 700; min-width: 110px; font-family: 'Courier New', monospace; font-size: 14px; padding-top: 2px; }
.t-row.accent .t-date { color: #38bdf8; }
.t-text { color: #c9d1d9; font-size: 15px; line-height: 1.5; }
.t-text strong { color: #e6edf3; }

/* 큰 숫자 hero */
.hero-num { font-size: 84px; font-weight: 900; line-height: 1; background: linear-gradient(135deg, #ef4444, #f97316); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-align: center; margin: 6px 0 8px; }
.hero-label { font-size: 16px; color: #8b949e; text-align: center; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 26px; }

/* U자 막대 차트 */
.bar-chart { display: flex; gap: 36px; align-items: flex-end; height: 220px; margin: 14px 0 24px; }
.bar-col { display: flex; flex-direction: column; align-items: center; gap: 10px; }
.bar { width: 110px; border-radius: 8px 8px 0 0; display: flex; align-items: flex-start; justify-content: center; padding-top: 10px; font-weight: 900; font-size: 18px; color: #e6edf3; }
.bar.high { height: 200px; background: linear-gradient(180deg, #34d399, rgba(52, 211, 153, 0.3)); }
.bar.low { height: 70px; background: linear-gradient(180deg, #ef4444, rgba(239, 68, 68, 0.3)); }
.bar-label { font-size: 13px; color: #8b949e; font-weight: 700; }

/* 태그 */
.tags { display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; margin-top: 18px; }
.tag {
  padding: 10px 22px; border: 1px solid rgba(124, 58, 237, 0.3); border-radius: 100px;
  background: rgba(124, 58, 237, 0.08); font-size: 14px; font-weight: 500; color: #c9d1d9;
}
.tag strong { color: #a78bfa; font-weight: 700; }

/* 네비 */
.slide-nav {
  position: fixed; bottom: 0; left: 0; right: 0; height: 50px;
  background: rgba(10, 15, 26, 0.95); backdrop-filter: blur(12px);
  border-top: 1px solid rgba(124, 58, 237, 0.2);
  display: flex; align-items: center; justify-content: center; z-index: 9999;
}
.slide-nav-inner { width: 1280px; display: flex; align-items: center; justify-content: space-between; padding: 0 60px; }
.slide-nav a { text-decoration: none; font-size: 14px; font-weight: 700; color: #7c3aed; transition: color 0.2s; }
.slide-nav a:hover { color: #a78bfa; }
.slide-nav .nav-disabled { font-size: 14px; font-weight: 700; color: #484f58; cursor: default; }
.slide-nav .nav-center a { color: #8b949e; font-size: 13px; font-weight: 400; }
.slide-nav .nav-center a:hover { color: #e6edf3; }

body { opacity: 0; animation: fadeIn 0.4s ease forwards; }
body.fade-out { animation: fadeOut 0.3s ease forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeOut { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(-12px); } }
"""

# ======================= 슬라이드 정의 =======================
# (num, slug, title, eyebrow, body_html, extra_css="")
SLIDES = []

def add(num, slug, title, eyebrow, body, extra_css=""):
    SLIDES.append((num, slug, title, eyebrow, body, extra_css))

# --- 01 cover ---
add(1, "cover", "AI에게 일을<br>시켜보다", None, """
<div class="kicker-big">VIBE CODING · 1강 (v2)</div>
<p class="cover-sub">결과가 매번 다르고 가끔 거짓말한다는 걸 — 자기 눈으로 본다</p>
<div class="tags">
  <span class="tag">단어 <strong>7개</strong></span>
  <span class="tag">함께 입력 <strong>6회</strong></span>
  <span class="tag">워크숍 <strong>130분</strong></span>
</div>
""", """
.title { font-size: 72px; line-height: 1.2; margin-bottom: 28px; }
.kicker-big { font-size: 16px; font-weight: 700; letter-spacing: 8px; color: #8b949e; margin-bottom: 22px; text-transform: uppercase; }
.cover-sub { font-size: 22px; color: #c9d1d9; text-align: center; margin-bottom: 50px; font-weight: 300; line-height: 1.6; }
""")

# --- 02 pomodoro-live ---
add(2, "pomodoro-live", "첫 라이브 — Pomodoro 타이머", "함께 입력 #1",
"""<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #1 — 모두 동시에</div>
  <div><span class="prompt-arrow">&gt;</span> 25분 집중 / 5분 휴식 사이클을 셀 수 있는 Pomodoro 타이머를 HTML 한 파일로 만들어줘</div>
</div>
<div class="callout">청중 50명 → <strong>50개의 다른 결과</strong> &nbsp;·&nbsp; 색·버튼 위치·소리·키보드 단축키… 모두 다름</div>
<p class="note">*"같은 한 줄을 시켰는데 — 왜 다 다르죠?"* &nbsp;이 질문이 오늘 130분의 입구입니다.</p>
""")

# --- 03 part1-cover ---
add(3, "part1-cover", "1부 — 바이브코딩이 뭔가", "PART 1 · 18분",
"""<p class="subtitle">단어 정의 → 1년 변천사 → 일상 매핑·Before/After·한국 사례 (3종 패키지)</p>
<div class="callout">약점 #2 보강 구간 — *정의는 들었지만 실감이 안 났다*</div>
""")

# --- 04 vibe-definition ---
add(4, "vibe-definition", "Karpathy의 트윗 한 줄", "정의",
"""<div class="code-box">2025-02-02  ·  Andrej Karpathy  ·  X (Twitter)

"There's a new kind of coding I call <span class="hl">'vibe coding'</span>,
where you fully give in to the vibes, embrace exponentials,
and forget that the code even exists."

— <span class="dim">샤워하다 떠오른 잡생각으로 던진 한 트윗 →
4,500만 회 조회, 6개월 만에 사전 등재</span>
</div>
<div class="callout">단어 자체에 이미 메시지가 박혀있어요 — *코드가 있다는 사실조차 잊는다*</div>
""")

# --- 05 vibe-1year ---
add(5, "vibe-1year", "1년 변천사", "TIMELINE",
"""<div class="timeline">
  <div class="t-row"><div class="t-date">2025-02</div><div class="t-text">Karpathy 트윗 — <strong>4,500만 조회</strong></div></div>
  <div class="t-row"><div class="t-date">2025-05</div><div class="t-text">Merriam-Webster <strong>사전 등재</strong> — *vibe coding* 정식 표제어</div></div>
  <div class="t-row"><div class="t-date">2025-후반</div><div class="t-text">한국 회사 도입 — Toss·당근·컬리 외부 공개 사례</div></div>
  <div class="t-row accent"><div class="t-date">2025-12</div><div class="t-text">Karpathy 본인 <strong>80% 위임</strong> — *변곡점*</div></div>
  <div class="t-row accent"><div class="t-date">2026-05</div><div class="t-text"><strong>Agentic Engineering</strong> 선언 — 다음 단계로</div></div>
</div>
<p class="note">트윗 → 사전 → 회사 → <strong>본인 변곡점</strong> → 다음 패러다임. <strong>1년 4개월</strong>의 가속.</p>
""")

# --- 06 vibe-analogy ---
add(6, "vibe-analogy", "외국 친구한테 김치찌개 시키기", "3종 패키지 A — 일상 비유",
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">옛날 방식 — 레시피 한 줄도 빠짐없이</span>
    <div class="comp-body">두부 200g, 신김치 300g 0.5cm로 썰고…<br>중불 5분, 고춧가루 1큰술…<br><br>→ 50줄짜리 레시피 정확히 작성<br>→ 한 단어 빠지면 망함</div>
  </div>
  <div class="comp-arrow">→</div>
  <div class="comp-side comp-new">
    <span class="comp-label">바이브 방식 — 한 마디</span>
    <div class="comp-body">"<code>얼큰하게, 두부 많이</code>"<br><br>→ 친구가 알아서 만들어옴<br>→ 100% 내 입맛은 아닐 수도<br>→ *결과가 나오는 속도*가 압도적</div>
  </div>
</div>
<p class="note">바이브코딩 = <strong>레시피 안 쓰고 분위기만 전달</strong>. 차이는 *완벽함*이 아니라 <strong>결과까지 가는 속도</strong>.</p>
""")

# --- 07 vibe-before-after ---
add(7, "vibe-before-after", "비개발자가 도구 1개 만들 때", "3종 패키지 B — Before / After",
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">2018 — 비개발자가 앱 만들기</span>
    <div class="comp-body">학원 6개월 등록<br>Python 책 1권<br>Stack Overflow 검색 지옥<br>→ <strong>3~6개월</strong> 후 *겨우* 동작<br>→ 중간에 80% 포기</div>
  </div>
  <div class="comp-arrow">→</div>
  <div class="comp-side comp-new">
    <span class="comp-label">2026 — Claude Code에 한 줄</span>
    <div class="comp-body">"<code>Pomodoro 타이머 만들어줘</code>"<br>5분 대기<br>→ <strong>5분</strong> 후 동작하는 HTML 한 파일<br>→ 수정도 *말로*</div>
  </div>
</div>
<p class="note">같은 도구 = 같은 결과. 차이는 <strong>도달 시간 × 1000배</strong>.</p>
""")

# --- 08 vibe-korea-cases ---
add(8, "vibe-korea-cases", "한국 회사 3곳", "3종 패키지 C — 실제 사례",
"""<div class="card-grid card-grid-3">
  <div class="card accent">
    <span class="card-num">Toss</span>
    <span class="card-title">전사 AI 도입</span>
    <span class="card-body">개발자/비개발자 가리지 않고 Claude·GPT 사내 표준화<br>2025년 후반 외부 발표</span>
  </div>
  <div class="card accent">
    <span class="card-num">당근</span>
    <span class="card-title">실무 워크플로우 재편</span>
    <span class="card-body">기획·디자인·고객 응대까지 LLM이 1차 초안<br>사람은 *검토·결정* 으로 역할 이동</span>
  </div>
  <div class="card accent">
    <span class="card-num">컬리</span>
    <span class="card-title">데이터 분석 자동화</span>
    <span class="card-body">SQL 작성·리포트 초안을 LLM이 담당<br>분석가는 *인사이트 해석*에 집중</span>
  </div>
</div>
<p class="note">공통점 — *코드 짜는 사람*만 쓰는 게 아니라 <strong>전사 도입</strong>. 비개발자도 같이 쓴다.</p>
""")

# --- 09 part2-cover ---
add(9, "part2-cover", "2부 — 단어 4개로 LLM의 정체", "PART 2 · 45분",
"""<p class="subtitle">LLM · 토큰 · 환각 · 비결정성 — 각 단어마다 *3종 패키지* 풀로</p>
<div class="callout">약점 #1 보강 구간 — 청중이 가장 못 그렸던 곳</div>
""")

# --- 10 llm-definition ---
add(10, "llm-definition", "LLM = 자동완성의 끝판왕", "단어 1 / 4 — 일상 비유",
"""<div class="code-box">LLM  =  Large Language Model
       <span class="dim">대규모 언어 모델</span>

본질  =  <span class="hl">다음에 올 단어를 예측하는 기계</span>

스마트폰 자동완성 :  "오늘 점심은…" → "?"
LLM (끝판왕)     :  같은 일을 <span class="hl">수십억 단어 학습</span> 후 수행
                   문장·문단·코드 단위까지 예측 확장</div>
<p class="note">본질은 한 줄 — <strong>다음에 가장 그럴듯한 단어</strong>를 *확률적으로* 잇는다. 그 이상도 이하도 아님.</p>
""")

# --- 11 llm-before-after ---
add(11, "llm-before-after", "단순 자동완성 vs LLM", "단어 1 / 4 — Before / After",
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">스마트폰 자동완성</span>
    <div class="comp-body">"오늘 점심은…"<br><br>→ 추천: <code>먹었어</code> / <code>뭐</code> / <code>괜찮아</code><br><br><strong>다음 한 단어</strong>까지</div>
  </div>
  <div class="comp-arrow">vs</div>
  <div class="comp-side comp-new">
    <span class="comp-label">LLM</span>
    <div class="comp-body">"오늘 점심은…"<br><br>→ "뭐 먹지? 매콤한 게 당기는데, 회사 근처에 김치찌개 잘하는 데 있어?"<br><br><strong>문단 + 맥락 + 질문</strong>까지</div>
  </div>
</div>
<p class="note">같은 *예측 기계* 가 — 학습량이 1억 배 늘면 결과가 <strong>차원이 달라짐</strong>.</p>
""")

# --- 12 llm-2026-lineup ---
add(12, "llm-2026-lineup", "2026-05 라인업", "단어 1 / 4 — 실제 사례",
"""<div class="card-grid card-grid-3">
  <div class="card accent">
    <span class="card-num">GPT-5</span>
    <span class="card-title">OpenAI</span>
    <span class="card-body">2025년 후반 출시<br>멀티모달·추론 강화<br>ChatGPT의 기본 엔진</span>
  </div>
  <div class="card accent">
    <span class="card-num">Claude 4.7</span>
    <span class="card-title">Anthropic</span>
    <span class="card-body">2026-04 출시<br>코딩·에이전트 작업 특화<br>오늘 실습 모델</span>
  </div>
  <div class="card accent">
    <span class="card-num">Gemini 2</span>
    <span class="card-title">Google</span>
    <span class="card-body">2026년 상반기<br>2M 토큰 컨텍스트 창<br>Google 생태계 통합</span>
  </div>
</div>
<p class="note">3사 모두 *같은 본질* (다음 단어 예측) 위에서 경쟁. <strong>강한 모델 = 더 그럴듯한 다음 단어</strong>.</p>
""")

# --- 13 tokenization-live ---
add(13, "tokenization-live", "토큰 — strawberry R 카운팅", "단어 2 / 4 — 라이브 시연 (함께 입력 #2)",
"""<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #2 — 청중 직접 확인</div>
  <div><span class="prompt-arrow">&gt;</span> strawberry라는 단어에 R이 몇 개 들어가?</div>
</div>
<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">사람의 시선</span>
    <div class="comp-body" style="font-family: 'Courier New', monospace; font-size: 20px; letter-spacing: 6px; text-align: center; padding: 8px 0;">s · t · <span style="color:#ef4444">r</span> · a · w · b · e · <span style="color:#ef4444">r</span> · <span style="color:#ef4444">r</span> · y</div>
    <div style="text-align:center; font-weight:900; color:#34d399; font-size:18px;">정답 — 3개</div>
  </div>
  <div class="comp-arrow">vs</div>
  <div class="comp-side comp-new">
    <span class="comp-label">LLM의 시선 (토큰)</span>
    <div class="comp-body" style="font-family:'Courier New',monospace; font-size:20px; text-align:center; padding:8px 0;"><span style="background:rgba(124,58,237,0.25); padding:4px 10px; border-radius:6px;">straw</span> + <span style="background:rgba(124,58,237,0.25); padding:4px 10px; border-radius:6px;">berry</span></div>
    <div style="text-align:center; font-weight:900; color:#ef4444; font-size:18px;">자주 — 2개라고 답함</div>
  </div>
</div>
<p class="note">덩어리(토큰) 안의 <strong>글자 하나하나는 못 본다</strong> — 이미 녹아 사라진 정보 위에서 추측.</p>
""")

# --- 14 tokenization-analogy ---
add(14, "tokenization-analogy", "한자 통째로 외운 사람", "단어 2 / 4 — 일상 비유",
"""<div class="callout">한자 <strong style="font-size:24px;">花</strong>(꽃 화) 글자에 — *점이 몇 개* 있나요?</div>
<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">사람 — 한자를 통째로 외움</span>
    <div class="comp-body" style="text-align:center; padding:8px 0;">
      <div style="font-size:64px; font-weight:900; color:#e6edf3; margin-bottom:8px;">花</div>
      <div style="font-size:13px; color:#8b949e;">글자=의미=발음 한 덩어리</div>
      <div style="margin-top:14px; font-size:14px;">점 개수를 세려면<br>→ <strong style="color:#a78bfa;">글자를 분해</strong>해야 함</div>
    </div>
  </div>
  <div class="comp-arrow">≈</div>
  <div class="comp-side comp-new">
    <span class="comp-label">LLM — 단어를 토큰 단위로 외움</span>
    <div class="comp-body" style="text-align:center; padding:8px 0;">
      <div style="font-size:24px; font-weight:900; color:#e6edf3; margin-bottom:8px;"><span style="background:rgba(124,58,237,0.25); padding:4px 10px; border-radius:6px;">straw</span> + <span style="background:rgba(124,58,237,0.25); padding:4px 10px; border-radius:6px;">berry</span></div>
      <div style="font-size:13px; color:#8b949e;">두 덩어리로 통째 외움</div>
      <div style="margin-top:14px; font-size:14px;">R 개수는<br>→ <strong style="color:#a78bfa;">출제 범위 밖</strong> 질문</div>
    </div>
  </div>
</div>
<p class="note">덩어리로 외워서 쓰는 사람에게 *글자 단위* 를 묻는 일 — <strong>가본 적 없는 길</strong>이라 추측한다.</p>
""")

# --- 15 tokenization-before-after ---
add(15, "tokenization-before-after", "공백 한 칸이 정답률을 바꾼다", "단어 2 / 4 — Before / After",
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">Before — 통덩어리</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"strawberry에 R 몇 개?"<br><br>→ <span style="color:#ef4444">2개 (틀림)</span></div>
  </div>
  <div class="comp-arrow">→</div>
  <div class="comp-side comp-new">
    <span class="comp-label">After — 글자 단위로 풀어 달라기</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"<code>s t r a w b e r r y</code>로 풀어서 R을 세줘"<br><br>→ <span style="color:#34d399">3개 (정답)</span></div>
  </div>
</div>
<p class="note">같은 모델 · 같은 단어 — <strong>공백 한 칸</strong> 차이로 정답률이 달라진다. 이게 *프롬프트 엔지니어링*의 핵심 직관.</p>
""")

# --- 16 hallucination-live ---
add(16, "hallucination-live", "환각 — 가짜 책 추천", "단어 3 / 4 — 라이브 시연 (함께 입력 #3)",
"""<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #3</div>
  <div><span class="prompt-arrow">&gt;</span> 2024년 노벨문학상 한국어 번역본 추천해줘. 책 제목·출판사·번역자까지.</div>
</div>
<div class="code-box">AI 응답 (예시)
"『○○○』 (○○출판사, 번역자 ○○○) — 2024년 출간"

→ 실제 검색  ::  <span class="bad">존재하지 않는 책</span>
→ 출판사     ::  <span class="bad">실재하나 그 책 안 냄</span>
→ 번역자     ::  <span class="bad">완전 허구</span>

<span class="hl">그럴듯한데, 거짓말</span>
</div>
<p class="note">이게 *환각* — 모르는 걸 *모른다*고 안 하고, <strong>그럴듯하게 만들어서</strong> 답함.</p>
""")

# --- 17 hallucination-analogy ---
add(17, "hallucination-analogy", "절대 모른다고 안 하는 신입", "단어 3 / 4 — 일상 비유",
"""<div class="callout">신입사원이 회의에서 — *"잘 모르겠는데요"* 를 절대 안 하는 사람.</div>
<div class="code-box">상사:  "지난주 매출 보고서 결론이 뭐였지?"

신입(좋은):  "아직 안 봤습니다. 확인하고 다시 답하겠습니다."

신입(환각):  "네, 전월 대비 12% 증가였고
            특히 30대 여성층이 ..."
            <span class="dim">← 들어본 적도 없음. 그냥 그럴듯하게 지어냄</span>

LLM 기본값  :  <span class="hl">두 번째 신입</span></div>
<p class="note">왜? — 학습 데이터에 *"모르겠어요"* 보다 *그럴듯한 답* 이 훨씬 많아서. 모델이 *그쪽을 더 잘 따라함*.</p>
""")

# --- 18 hallucination-before-after ---
add(18, "hallucination-before-after", '*"모르면 모른다고 답해"*', "단어 3 / 4 — Before / After",
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">Before</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"한국 변호사법 17조 알려줘"<br><br>→ <span style="color:#ef4444">존재하지 않는 조항을 그럴듯하게 작성</span></div>
  </div>
  <div class="comp-arrow">→</div>
  <div class="comp-side comp-new">
    <span class="comp-label">After — 거절 허용 명시</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"한국 변호사법 17조 알려줘.<br>모르면 *모른다*고 답해.<br>출처 URL 없으면 답하지 마."<br><br>→ <span style="color:#34d399">"확인된 출처가 없어 답하지 못합니다"</span></div>
  </div>
</div>
<p class="note">한 줄 추가 — *"모르면 모른다"·"출처 없으면 답하지 마"*. 환각의 90%를 잡아내는 단순한 룰.</p>
""")

# --- 19 hallucination-mata-avianca ---
add(19, "hallucination-mata-avianca", "Mata v. Avianca 사건", "단어 3 / 4 — 실제 사건",
"""<div class="hero-label">2023 · 5월 · 미국 뉴욕 남부지방법원</div>
<div class="hero-num">$5,000</div>
<div style="text-align:center; font-size:15px; color:#8b949e; margin-bottom:24px;">변호사 + 로펌 벌금 &nbsp;·&nbsp; 30년 경력 변호사 Steven Schwartz</div>
<div class="card-grid card-grid-2">
  <div class="card">
    <span class="card-num" style="color:#ef4444;">사건</span>
    <span class="card-title">ChatGPT로 판례 6건 작성</span>
    <span class="card-body">법원 제출 → 판사 검색 → <strong style="color:#ef4444;">6건 모두 존재하지 않음</strong></span>
  </div>
  <div class="card">
    <span class="card-num" style="color:#ef4444;">2차 환각</span>
    <span class="card-title">"이 판례 진짜냐?" 재확인</span>
    <span class="card-body">ChatGPT가 *"진짜"* 라고 답함 → 변호사 그 답변까지 그대로 제출</span>
  </div>
</div>
<p class="note">환각 = *재미난 실수* 가 아니라 — <strong>법정에서 벌금 맞는 일</strong>. 미국 모든 법대 강의에 등장하는 사례.</p>
""")

# --- 20 non-determinism-live ---
add(20, "non-determinism-live", "비결정성 — 같은 prompt 3회", "단어 4 / 4 — 라이브 (함께 입력 #4)",
"""<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #4 — 같은 한 줄을 3번 반복</div>
  <div><span class="prompt-arrow">&gt;</span> 비 오는 날 카페에 앉아 있는 30대 여성을 한 문단으로 묘사해줘</div>
</div>
<div class="card-grid card-grid-3">
  <div class="card"><span class="card-num">1회</span><span class="card-body">창가 자리, 따뜻한 라떼, 노트북…</span></div>
  <div class="card"><span class="card-num">2회</span><span class="card-body">우산 접은 채 들어와, 책 한 권…</span></div>
  <div class="card"><span class="card-num">3회</span><span class="card-body">통화 중인 옆모습, 비 소리…</span></div>
</div>
<p class="note">같은 모델 · 같은 한 줄 · 다른 답. <strong>옆 사람과 비교</strong>해보세요 — 50명 = 50개의 카페.</p>
""")

# --- 21 non-determinism-temperature ---
add(21, "non-determinism-temperature", "온도 (temperature) — 우연의 폭", "단어 4 / 4 — Before/After + 비유",
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">temperature = 0</span>
    <div class="comp-body">매번 같은 답<br>→ *결정론적*<br>→ 분류·번역·정답 있는 작업</div>
  </div>
  <div class="comp-arrow">~</div>
  <div class="comp-side comp-new">
    <span class="comp-label">temperature = 0.7 (Claude Code 기본)</span>
    <div class="comp-body">매번 살짝 다른 답<br>→ *창의성·다양성*<br>→ 글쓰기·아이디어·코드 변형</div>
  </div>
</div>
<div class="callout"><strong>일상 비유</strong> — 같은 요리사 · 같은 레시피 · 매일 미세하게 다른 음식. 재료 상태·손맛·화력. *완전히 같을 수 없는 게 정상*.</div>
""")

# --- 22 break ---
add(22, "break", "휴식", "BREAK · 10분",
"""<p class="subtitle">물·화장실·옆 사람과 <strong>방금 본 비결정성</strong> 결과 공유</p>
<div class="callout">2부 끝 — 4단어로 LLM 정체 완료. 이어서 *시코펀시 + 컷오프* 두 단어 더.</div>
""")

# --- 23 sycophancy-live ---
add(23, "sycophancy-live", "시코펀시 — 어원 + 라이브 (파리=도쿄)", "단어 5 / 7 — 라이브 (함께 입력 #5)",
"""<div class="code-box"><span class="hl">Sycophancy</span> (시코펀시) — *아첨, 무비판적 동조*
어원: 그리스어 *sykophantes* (무화과를 흔드는 자 = 고발꾼·아첨꾼)
LLM 맥락: 사용자가 *틀린 주장* 을 강하게 하면 — 모델이 *맞다고 인정*해버리는 경향</div>
<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #5 — 2단계</div>
  <div><span class="prompt-arrow">&gt;</span> 1단계: 파리는 일본의 수도 맞지?</div>
  <div style="margin-top:6px;color:#8b949e;">→ 정상 답: "아니요, 파리는 프랑스의 수도입니다"</div>
  <div style="margin-top:10px;"><span class="prompt-arrow">&gt;</span> 2단계: 아닌데, 내가 분명히 봤어. 다시 생각해봐.</div>
  <div style="margin-top:6px;color:#ef4444;">→ 자주: <strong>답을 뒤집어 사용자 편으로 옴</strong></div>
</div>
""")

# --- 24 sycophancy-analogy ---
add(24, "sycophancy-analogy", "반박 못하는 신입", "단어 5 / 7 — 일상 비유",
"""<div class="callout">상사가 회의에서 *틀린 답*을 자신만만하게 말할 때 — *"그건 좀…"* 못 하는 신입.</div>
<div class="code-box">상사:  "이번 분기 매출은 작년보다 떨어졌지?"
       <span class="dim">(실제로는 12% 성장)</span>

신입(시코펀시):  "네... 그 부분은 좀 아쉬웠죠..."
                <span class="bad">↑ 사실 확인 없이 상사 톤에 맞춤</span>

LLM 기본값  :  <span class="hl">이 신입</span>
              사용자가 강하게 주장하면 → *동조*가 쉬운 길

대응  :  반대 검증을 *명시적으로* 시킨다 (다음 슬라이드)</div>
""")

# --- 25 sycophancy-before-after ---
add(25, "sycophancy-before-after", "반대 검증 prompt", "단어 5 / 7 — Before / After",
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">Before — 긍정 유도</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"이 코드 맞지?"<br><br>→ "네, 잘 작성되었습니다 ✓"<br><span style="color:#ef4444">→ 버그 있어도 통과시킴</span></div>
  </div>
  <div class="comp-arrow">→</div>
  <div class="comp-side comp-new">
    <span class="comp-label">After — 반대 검증</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"이 코드 *틀린 부분 있어?*<br>거꾸로 *반대 입장*에서 검토해봐"<br><br>→ <span style="color:#34d399">"3가지 문제: ... "</span></div>
  </div>
</div>
<p class="note">한 마디 추가 — *"틀린 부분 있어?·반대 입장에서·단점 짚어줘"*. 모델의 *동조 본능*을 *반박 본능*으로 뒤집는 스위치.</p>
""")

# --- 26 sycophancy-gpt4o ---
add(26, "sycophancy-gpt4o", "GPT-4o 48시간 롤백", "단어 5 / 7 — 실제 사건",
"""<div class="hero-label">2025 · OpenAI · GPT-4o 업데이트</div>
<div class="hero-num">48시간</div>
<div style="text-align:center; font-size:15px; color:#8b949e; margin-bottom:22px;">배포 → 롤백 &nbsp;·&nbsp; CEO Sam Altman 공개 사과</div>
<div class="timeline">
  <div class="t-row"><div class="t-date">04-25</div><div class="t-text">업데이트 배포 — *극도의 아부 모드*<br><span style="color:#8b949e; font-size:13px;">"당신 말이 100% 맞아요" · 위험한 결정에도 박수 · 사실관계 틀려도 동조</span></div></div>
  <div class="t-row"><div class="t-date">~24h</div><div class="t-text">소셜 미디어 폭발 — 스크린샷 <strong>수만 건</strong> 공유</div></div>
  <div class="t-row accent"><div class="t-date">04-28</div><div class="t-text"><strong>롤백 발표</strong> — *"튜닝 과정에서 시코펀시 가중이 과도했다"*</div></div>
</div>
<p class="note">시코펀시는 *친절함*과 분리하기 까다로움 — <strong>인류 최대 LLM 회사가 4일 만에 롤백</strong>한 사건.</p>
""")

# --- 27 cutoff-live ---
add(27, "cutoff-live", "지식 컷오프 — 어제 뉴스", "단어 6 / 7 — 라이브 (함께 입력 #6)",
"""<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #6</div>
  <div><span class="prompt-arrow">&gt;</span> 오늘 서울 날씨 알려줘. 그리고 어제 한국 뉴스 1면이 뭐였어?</div>
</div>
<div class="code-box">AI 응답  :  "<span class="dim">제가 마지막으로 학습한 정보는 2026년 1월까지이며,
            오늘 날씨나 어제 뉴스에 대한 실시간 정보는 알 수 없습니다.</span>"

→ 좋은 답  ::  <span class="ok">모른다고 인정</span>
→ 나쁜 답  ::  <span class="bad">학습 시점 뉴스를 어제 뉴스인 양 답함 (= 환각)</span>

Claude 4.7 컷오프  =  <span class="hl">2026-01</span>
오늘                =  <span class="hl">2026-05-10</span>
                    →  *5개월 깜깜한 구간*</div>
""")

# --- 28 cutoff-before-after ---
add(28, "cutoff-before-after", "본문 첨부 후 묻기", "단어 6 / 7 — 일상 비유 + Before/After",
"""<div class="callout"><strong>일상 비유</strong> — *작년 인쇄된 백과사전*을 들고 다니는 천재 학생 / *어제 신문 못 읽고* 출근한 직원.</div>
<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">Before — 컷오프 너머 직접 질문</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"2026-04 출시된 Claude 4.7 특징은?"<br><br>→ <span style="color:#ef4444">추측·환각</span> (학습 시점 외)</div>
  </div>
  <div class="comp-arrow">→</div>
  <div class="comp-side comp-new">
    <span class="comp-label">After — 기사 본문 첨부 후</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"<code>[Anthropic 공식 발표 본문 붙여넣기]</code><br>위 발표 핵심 3가지 요약해줘"<br><br>→ <span style="color:#34d399">정확한 요약</span></div>
  </div>
</div>
<p class="note">같은 모델 · 같은 컷오프 — <strong>본문을 같이 주냐</strong> 차이. 이게 *컨텍스트 엔지니어링*의 가장 작은 사례.</p>
""")

# --- 29 design-not-luck ---
add(29, "design-not-luck", "우연이 아니라 설계", "5부 진입",
"""<p class="subtitle" style="font-size:22px;">지금까지 본 모든 한계 — *그래서 어떻게 하나*</p>
<div class="callout" style="font-size:20px; padding:24px;">같은 AI에게 <strong>좋은 답이 나올 확률</strong>을 — <br><strong style="color:#a78bfa;">우연</strong> 이 아니라 <strong style="color:#38bdf8;">설계</strong> 로 끌어올린다.</div>
<p class="note">설계 도구가 *3개 동심원* — 다음 슬라이드부터 4장 연속.</p>
""")

# --- 30 three-circles-overview ---
add(30, "three-circles-overview", "3-동심원 — 셋 다 동시에", "약점 #3 핵심 1 / 4",
"""<div class="three-circles">
  <div class="circle circle-outer">하니스</div>
  <div class="circle circle-mid">컨텍스트</div>
  <div class="circle circle-inner">프롬프트</div>
</div>
<p class="note" style="font-size:17px;"><strong style="color:#f9a8d4">프롬프트</strong> ⊂ <strong style="color:#a78bfa">컨텍스트</strong> ⊂ <strong style="color:#38bdf8">하니스</strong> &nbsp;·&nbsp; *일자가 아니라 동심원*. 셋 다 *항상 동시에* 박혀있다.</p>
""")

# --- 31 three-circles-lawyer ---
add(31, "three-circles-lawyer", "변호사에게 사건 맡기기", "약점 #3 핵심 2 / 4 — 일상 비유",
"""<div class="card-grid card-grid-3">
  <div class="card" style="background:rgba(236,72,153,0.08); border-color:rgba(236,72,153,0.3);">
    <span class="card-num" style="color:#f9a8d4;">프롬프트</span>
    <span class="card-title">한 마디 부탁</span>
    <span class="card-body">*"이 계약서 검토해줘"*</span>
  </div>
  <div class="card" style="background:rgba(167,139,250,0.08); border-color:rgba(167,139,250,0.3);">
    <span class="card-num" style="color:#a78bfa;">컨텍스트</span>
    <span class="card-title">함께 건네는 자료</span>
    <span class="card-body">사건 개요 + 관련 판례 + 증거 자료를 *같이* 건넴</span>
  </div>
  <div class="card" style="background:rgba(56,189,248,0.08); border-color:rgba(56,189,248,0.3);">
    <span class="card-num" style="color:#38bdf8;">하니스</span>
    <span class="card-title">일이 굴러가는 환경</span>
    <span class="card-body">사무실·비서·로펌 DB·동료 검토 — *전체 시스템*</span>
  </div>
</div>
<p class="note">변호사가 잘하려면 <strong>셋 다 필요</strong>. 한 마디만 던지면 부족, 자료만 줘도 부족, 환경만 좋아도 부족.</p>
""")

# --- 32 three-circles-before-after ---
add(32, "three-circles-before-after", "코드 짜기 — 3단계", "약점 #3 핵심 3 / 4 — Before / After",
"""<div class="card-grid card-grid-3">
  <div class="card">
    <span class="card-num" style="color:#f9a8d4;">1단계</span>
    <span class="card-title">프롬프트만</span>
    <span class="card-body" style="font-family:'Courier New',monospace; font-size:12px;">"<code>코드 짜줘</code>"<br><br>→ 일반적·평범함</span>
  </div>
  <div class="card">
    <span class="card-num" style="color:#a78bfa;">2단계</span>
    <span class="card-title">+ 컨텍스트</span>
    <span class="card-body" style="font-family:'Courier New',monospace; font-size:12px;">"코드 스타일 가이드 첨부.<br>이 함수 흉내 내서 짜줘"<br><br>→ *우리 회사스러움*</span>
  </div>
  <div class="card accent">
    <span class="card-num" style="color:#38bdf8;">3단계</span>
    <span class="card-title">+ 하니스</span>
    <span class="card-body" style="font-family:'Courier New',monospace; font-size:12px;">Claude Code가<br>짜고 → 테스트 돌리고<br>→ 실패하면 *자기가 고침*<br><br>→ *동작 보장*</span>
  </div>
</div>
<p class="note">한 단계씩 갈수록 — <strong>같은 모델인데 결과 신뢰도가 누적</strong>. 셋 중 *하나만* 쓰는 게 아니라 *셋 다 동시에*.</p>
""")

# --- 33 three-circles-pomodoro ---
add(33, "three-circles-pomodoro", "같은 화면에 셋 다 박혀있다", "약점 #3 핵심 4 / 4 — Pomodoro 회수",
"""<div class="code-box"><span class="dim">[Claude Code 세션 화면]</span>

<span style="color:#f9a8d4">┃ 프롬프트 (가장 안쪽)</span>
<span style="color:#f9a8d4">┃ &gt; "Pomodoro 타이머 만들어줘"</span>

<span style="color:#a78bfa">┃ 컨텍스트 (감싸는 층)</span>
<span style="color:#a78bfa">┃   - CLAUDE.md (이 프로젝트는…)</span>
<span style="color:#a78bfa">┃   - 첨부 파일·검색 결과·이전 대화</span>

<span style="color:#38bdf8">┃ 하니스 (모두 감싸는 환경)</span>
<span style="color:#38bdf8">┃   - 도구: 파일 읽기·쓰기·실행</span>
<span style="color:#38bdf8">┃   - 권한 시스템·자동 검증·서브에이전트</span>
<span style="color:#38bdf8">┃   - 세션 관리·체크포인트</span>

→ <span class="hl">우리가 첫 라이브에서 본 그 한 줄 결과</span> = 셋이 동시에 일한 결과</div>
<p class="note">*"오늘 처음에 본 그 마법"* = 동심원 셋이 한 화면에서 같이 일한 결과.<br><strong>셋이 분리된 게 아니라 — 겹쳐 있다.</strong></p>
""")

# --- 34 prompt-engineering-4patterns ---
add(34, "prompt-engineering-4patterns", "프롬프트 엔지니어링 — 4기법", "6부 · 동심원 가장 안쪽",
"""<div class="card-grid card-grid-2">
  <div class="card">
    <span class="card-num">Zero-shot</span>
    <span class="card-title">예시 없이 시키기</span>
    <span class="card-body" style="font-family:'Courier New',monospace; font-size:12px;">"이 문장을 영어로 번역해줘"</span>
  </div>
  <div class="card">
    <span class="card-num">Few-shot</span>
    <span class="card-title">예시 한두 개 주기</span>
    <span class="card-body" style="font-family:'Courier New',monospace; font-size:12px;">"'안녕'→'Hello'.<br>그러면 '잘가'는?"</span>
  </div>
  <div class="card">
    <span class="card-num">Chain-of-Thought</span>
    <span class="card-title">단계별로 풀어달라기</span>
    <span class="card-body" style="font-family:'Courier New',monospace; font-size:12px;">"단계별로 생각해서<br>답해줘"</span>
  </div>
  <div class="card">
    <span class="card-num">Role</span>
    <span class="card-title">역할 부여</span>
    <span class="card-body" style="font-family:'Courier New',monospace; font-size:12px;">"너는 시니어 변호사야.<br>이 계약서 봐줘"</span>
  </div>
</div>
<div class="callout">한 마디 추가하느냐 — <strong>마느냐</strong>. 답의 정확도를 <strong>30~50%</strong> 바꾼다.<br>*질문을 잘 던지는 능력*이 — 새로운 기술이 됐다.</div>
""")

# --- 35 context-engineering-5elements ---
add(35, "context-engineering-5elements", "컨텍스트 엔지니어링 — 5요소", "6부 · 동심원 가운데",
"""<div class="code-box">컨텍스트 = AI가 답하기 직전에 *보고 있는 모든 것* (한 덩어리로 들어감)

<span class="hl">1. 시스템 지시문</span>     "너는 친절한 한국어 비서야. 출처 없으면 답하지 마"
<span class="hl">2. 사용자 질문</span>       우리가 입력한 그 한 줄
<span class="hl">3. 자동 검색 자료</span>     답하기 전에 AI가 직접 찾아온 관련 문서  (← RAG)
<span class="hl">4. 도구 사용 결과</span>     코드 실행 결과·외부 서비스 응답·파일 읽기
<span class="hl">5. 이전 대화 요약</span>     길어진 대화를 압축한 메모</div>
<div class="callout">Karpathy (2025-06-24): *"매 단계마다 컨텍스트 창에 정확히 맞는 정보를 채우는 <strong>섬세한 예술이자 과학</strong>"*</div>
""")

# --- 36 lost-in-the-middle ---
add(36, "lost-in-the-middle", "Lost in the Middle — 가운데에서 길을 잃다", "컨텍스트 함정",
"""<div class="hero-label">Stanford · 2023 · Liu et al. (arXiv:2307.03172)</div>
<div class="bar-chart">
  <div class="bar-col"><div class="bar high">정확</div><div class="bar-label">맨 앞</div></div>
  <div class="bar-col"><div class="bar low">20~30%</div><div class="bar-label">한가운데</div></div>
  <div class="bar-col"><div class="bar high">정확</div><div class="bar-label">맨 끝</div></div>
</div>
<div style="text-align:center; font-size:14px; color:#8b949e; margin-bottom:20px; letter-spacing:2px;">U 자 모양 성능 곡선 &nbsp;·&nbsp; 창이 길수록 가운데 효과 ↑</div>
<div class="callout"><strong>일상 비유</strong> — 2시간 회의록의 *처음 10분·마지막 10분*은 또렷, *가운데*는 흐릿. LLM도 같은 <strong>U자 모양 기억력</strong>.</div>
<p class="note">컨텍스트 엔지니어링 = "많이 넣기"가 아니라 — <strong>무엇을, 어느 위치에</strong> 까지 다루는 일.</p>
""")

# --- 37 harness-etymology ---
add(37, "harness-etymology", "하니스 — 어원부터", "6부 · 동심원 가장 바깥",
"""<div class="code-box">Harness  (영어, 명사)

  1) <span class="hl">마구(馬具)</span> — 말의 힘을 마차나 쟁기에
                  *유용한 일에 쓰도록* 매다는 도구

  2) 등산 안전벨트·낙하산 멜빵
                  사람을 줄·장비에 *안전하게* 잇는 띠

  3) <span class="hl">test harness</span> (소프트웨어)
                  코드를 *둘러싸고* 자동 실행·검증하는 틀</div>
<div class="callout">Anthropic 공식: *"하니스는 모델 그 자체가 아닌 모든 코드·설정·실행 로직이다"*<br>— 모델은 그대로, <strong>나머지 전부</strong>가 하니스.</div>
""")

# --- 38 model-cant-do-alone ---
add(38, "model-cant-do-alone", "AI 혼자서는 안 되는 일 4가지", "왜 한 층 더 둘러야 하나",
"""<div class="card-grid card-grid-2">
  <div class="card"><span class="card-num">1</span><span class="card-title">실행해서 검증 불가</span><span class="card-body">코드 짜줘도 *돌려보고 결과 확인*할 손이 없다</span></div>
  <div class="card"><span class="card-num">2</span><span class="card-title">자기 답 재확인 불가</span><span class="card-body">답하고도 *다시 점검*할 도구 없음 → 가짜책·Mata 사건 (16·19)</span></div>
  <div class="card"><span class="card-num">3</span><span class="card-title">컨텍스트 끊기면 망각</span><span class="card-body">세션 닫으면 *어제 약속* 사라짐</span></div>
  <div class="card"><span class="card-num">4</span><span class="card-title">한 시간+ 흐름 못 끌고 감</span><span class="card-body">3단계만 넘어가도 *처음 약속* 흘림</span></div>
</div>
<div class="callout"><strong>일상 비유</strong> — 천재 인턴이 *책상·컴퓨터·회의록·동료 검토자 없이* 빈 방에 혼자. 결과를 신뢰하기 어려움.</div>
""")

# --- 39 harness-4axis ---
add(39, "harness-4axis", "하니스 4축 — 도구·반복·검증·기억", "비개발자용 4단어",
"""<div class="card-grid card-grid-2">
  <div class="card accent"><span class="card-num">도구 (Tools)</span><span class="card-title">세계로 손 뻗기</span><span class="card-body">파일 읽기·코드 실행·웹 검색<br>→ 한계 (1) 해결</span></div>
  <div class="card accent"><span class="card-num">반복 (Loop)</span><span class="card-title">다시 시도</span><span class="card-body">결과 보고, 고치고, 또 돌리기<br>→ 한계 (4) 해결</span></div>
  <div class="card accent"><span class="card-num">검증 (Verify)</span><span class="card-title">별도 점검자</span><span class="card-body">짜는 AI / 검토 AI / 채점 AI<br>→ 한계 (2) 해결</span></div>
  <div class="card accent"><span class="card-num">기억 (Memory)</span><span class="card-title">세션 너머 지속</span><span class="card-body">파일·docs로 영속화<br>→ 한계 (3) 해결</span></div>
</div>
<p class="note">첫 라이브 Pomodoro에서 — <strong>4축이 동시에</strong> 일했어요.<br>청중은 *"AI가 한 번에 만들었네"* 라고 봤지만, 사실 4축이 같이 굴러간 결과.</p>
""")

# --- 40 part7-cover ---
add(40, "part7-cover", "7부 — 도구", "PART 7 · 10분",
"""<p class="subtitle" style="font-size:20px;">동심원·5요소·하니스 4축이 — *이미 다 박혀 있는 도구 한 개*</p>
<div class="callout" style="padding:22px; font-size:18px;">오늘 우리가 처음에 한 번 같이 써본 그것 — <br>이 마지막 10분, 그 도구의 <strong>4가지 부품</strong>을 짧게.</div>
""")

# --- 41 what-is-claude-code ---
add(41, "what-is-claude-code", "Claude Code가 뭔가", "도구 · 정의",
"""<div class="code-box"><span class="hl">Claude Code</span>  ·  Anthropic 공식 CLI
2025-02 첫 출시  ·  2026-05 기준 2.x 버전

한 줄 정의
  터미널에 *자연어*로 부탁하면 — AI가 직접
  파일을 읽고, 고치고, 명령을 실행해주는 도구

웹 챗봇과 결정적 차이  :  <span class="hl">손을 직접 움직인다</span></div>
<div class="callout"><strong>일상 비유</strong> — 챗봇이 *"조언자"* (옆에서 말로) 라면 Claude Code는 *"동료 개발자"* (내 책상에 앉아 직접 일).</div>
<p class="note">오늘 이미 한 번 써봤어요 → 슬라이드 <strong>02</strong> Pomodoro. <strong>그게 Claude Code였습니다</strong>.</p>
""")

# --- 42 why-cli ---
add(42, "why-cli", "왜 까만 화면이어야 하나", "도구 · CLI vs 웹",
"""<div class="code-box">                       claude.ai (웹)   Claude Code (CLI)
─────────────────────────────────────────────────────
글로 묻고 답 받기            <span class="ok">✅</span>            <span class="ok">✅</span>
내 컴퓨터 파일 읽기          <span class="bad">❌</span>            <span class="ok">✅</span>
내 컴퓨터 파일 수정          <span class="bad">❌</span>            <span class="ok">✅</span>
명령 실행 (빌드/테스트)      <span class="bad">❌</span>            <span class="ok">✅</span>
작업 자동화·반복             <span class="bad">❌</span>            <span class="ok">✅</span>

→ 5축 차이.  하니스 4축(반복·검증·기억·도구)이 살 수 있는 무대 = <span class="hl">CLI</span></div>
<div class="callout"><strong>레스토랑 vs 주방</strong> — 채팅창=손님이 주문하는 *홀*. CLI=주방, 직접 재료를 만지고 그릇에 담는다.</div>
<p class="note"><strong>안심</strong> — 명령 거의 안 외워도 됨(자연어 그대로) · 잘못 쳐도 <code>/sandbox·/permissions</code>가 차단 · 잘못한 결정은 <code>/rewind</code>로 되돌리기.</p>
""")

# --- 43 claude-md ---
add(43, "claude-md", "CLAUDE.md — 한 장의 사용설명서", "부품 1 · 매 세션 자동 로드",
"""<div class="code-box">프로젝트 루트/
├── <span class="hl">CLAUDE.md</span>   ← 매 세션 자동으로 컨텍스트에 들어감
├── src/
└── docs/

[안에 무엇을 넣나]
  1. 이 프로젝트가 무엇인가     (한 단락)
  2. 사용 기술 스택과 규칙       ("들여쓰기 4칸, 타입 힌트 필수")
  3. 자주 쓰는 명령              ("pnpm dev", "make test")
  4. AI에게 시키면 안 되는 일    ("production/ 폴더 직접 수정 금지")
  5. 선호 톤·언어                ("답변은 한국어로")</div>
<div class="callout"><strong>일상 비유</strong> — 새 직원이 첫 출근날 받는 *팀 룰북*.<br>매번 옆 사람에게 다시 물을 필요 없게 — <strong>한 장의 영속 컨텍스트</strong>.</div>
""")

# --- 44 skill ---
add(44, "skill", "Skill — 자주 쓰는 작업에 이름표", "부품 2 · 슬래시 한 번에 호출",
"""<div class="code-box">~/.claude/skills/
└── presentation_script/
    └── <span class="hl">SKILL.md</span>           ← frontmatter + 지시문

호출  :  <span class="hl">&gt; /presentation_script</span>
        → 미리 박아둔 절차 + 프롬프트가 한 번에 실행</div>
<div class="callout"><strong>일상 비유</strong> — 회사 보고서 *템플릿 라이브러리*. 매번 *빈 워드*에서 시작 → 한 번에 불러옴.</div>
<p class="note">이 강의 레포에도 살아 있어요 — <code>/presentation_slides</code> · <code>/harness</code> · <code>/review</code>.<br>2강에서 *직접 한 장 만들어보는* 시간이 있어요.</p>
""")

# --- 45 mcp-and-subagents ---
add(45, "mcp-and-subagents", "MCP · 서브에이전트", "부품 3+4 · 외부 연결과 분업",
"""<div class="card-grid card-grid-2">
  <div class="card accent">
    <span class="card-num">MCP</span>
    <span class="card-title">AI 통합의 USB-C</span>
    <span class="card-body">Anthropic 2024-11 공개<br>2025-12 Linux Foundation 기증<br>→ Kubernetes·PyTorch와 같은 *중립 인프라*<br><br>GitHub·Figma·Slack·DB를<br>한 가지 형식으로 LLM에 연결</span>
  </div>
  <div class="card accent">
    <span class="card-num">서브에이전트</span>
    <span class="card-title">회사의 부서</span>
    <span class="card-body">메인 Claude = PM<br>각 서브에이전트 = 디자인팀·개발팀·QA팀<br><br>각자 *컨텍스트 창·시스템 프롬프트·도구 권한·모델*<br>(빠른 일=Haiku, 무거운 일=Opus)</span>
  </div>
</div>
<div class="callout"><strong>오늘 메시지</strong> — 동심원 · 5요소 · 하니스 4축이<br><strong>모두 이 한 도구 안에 박혀있다</strong></div>
""")

# --- 46 live-round ---
add(46, "live-round", "라이브 라운드 — 청중이 만들고 싶은 도구", "8부 · 함께 입력 #7",
"""<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #7 — 청중 1명에게 받은 도구 요청</div>
  <div><span class="prompt-arrow">&gt;</span> [청중이 즉석에서 제안한 도구 한 줄]</div>
</div>
<div class="callout">전 청중 동시 입력 → 50개의 다른 결과 → 토론</div>
<div class="code-box">토론 질문 (강사 진행)
  Q1.  결과가 다 다르죠? → <span class="hl">비결정성</span> 다시 보임
  Q2.  방금 본 어떤 LLM 한계가 여기서 보이나요?
       → 토큰? 환각? 시코펀시? 컷오프? Lost in the Middle?
  Q3.  이걸 *우연이 아닌 설계*로 끌어올리려면
       — 프롬프트? 컨텍스트? 하니스? 어디를 만져야?</div>
""")

# --- 47 closing-7words ---
add(47, "closing-7words", "단어 7개 + 동심원 한 장", "9부 · 마무리",
"""<div class="card-grid card-grid-4" style="max-width:1100px;">
  <div class="card"><span class="card-num">1</span><span class="card-title">바이브코딩</span></div>
  <div class="card"><span class="card-num">2</span><span class="card-title">LLM</span></div>
  <div class="card"><span class="card-num">3</span><span class="card-title">토큰</span></div>
  <div class="card"><span class="card-num">4</span><span class="card-title">환각</span></div>
  <div class="card"><span class="card-num">5</span><span class="card-title">비결정성</span></div>
  <div class="card"><span class="card-num">6</span><span class="card-title">시코펀시</span></div>
  <div class="card"><span class="card-num">7</span><span class="card-title">지식 컷오프</span></div>
  <div class="card accent"><span class="card-num" style="color:#38bdf8;">+</span><span class="card-title">3-동심원</span><span class="card-body">프롬프트 ⊂ 컨텍스트 ⊂ 하니스</span></div>
</div>
<div class="callout">단어 7개 + 동심원 한 장 — 이 한 슬라이드가 <strong>오늘 130분의 압축</strong></div>
""")

# --- 48 next-lecture ---
add(48, "next-lecture", "다음 강의 예고 — 2강", "9부 · 마무리",
"""<p class="subtitle">하니스 세팅 — 이미 박혀 있는 1층 위에 내 프로젝트 2층 한 층 더 올리기</p>
<div class="card-grid card-grid-2">
  <div class="card accent">
    <span class="card-num">2층 4가지</span>
    <span class="card-title">CLAUDE.md / docs / skills / hooks</span>
    <span class="card-body">한 층 올린다는 것 — 4종 markdown만 손봐도 충분</span>
  </div>
  <div class="card accent">
    <span class="card-num">클라이맥스</span>
    <span class="card-title">claude -p 매커니즘</span>
    <span class="card-body">CI/CD에 헤드리스 Claude 끼워넣기</span>
  </div>
</div>
<div class="callout">3강 = Dicom Viewer 만들기 (5단계 워크플로우 라이브)</div>
<p class="note" style="margin-top:24px; color:#c9d1d9;">감사합니다 — 오늘 1강 끝.</p>
""")

# ======================= 렌더링 =======================
def render_slide(num, slug, title, eyebrow, body, extra_css):
    fname = f"{num:02d}-{slug}.html"
    prev_fname = SLIDES[num-2][0:2] if num > 1 else None
    next_fname = SLIDES[num][0:2] if num < TOTAL else None

    if prev_fname:
        prev_link = f'<a href="{prev_fname[0]:02d}-{prev_fname[1]}.html" onclick="event.preventDefault(); navigateTo(this.href)">&larr; 이전</a>'
        prev_js = f"  if (e.key === 'ArrowLeft') navigateTo('{prev_fname[0]:02d}-{prev_fname[1]}.html');"
    else:
        prev_link = '<span class="nav-disabled">&larr; 이전</span>'
        prev_js = ""

    if next_fname:
        next_link = f'<a href="{next_fname[0]:02d}-{next_fname[1]}.html" onclick="event.preventDefault(); navigateTo(this.href)">다음 &rarr;</a>'
        next_js = f"  if (e.key === 'ArrowRight') navigateTo('{next_fname[0]:02d}-{next_fname[1]}.html');"
    else:
        next_link = '<span class="nav-disabled">다음 &rarr;</span>'
        next_js = ""

    eyebrow_html = f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''
    title_html = f'<h1 class="title">{title}</h1>' if title else ''

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>{title.replace('<br>', ' ')} — v2/1강</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
{COMMON_CSS}
{extra_css}
</style>
</head>
<body>
<div class="container">
  {eyebrow_html}
  {title_html}
  {body}
</div>

<nav class="slide-nav">
  <div class="slide-nav-inner">
    <div class="nav-left">{prev_link}</div>
    <div class="nav-center"><a href="index.html">{num:02d} / {TOTAL}</a></div>
    <div class="nav-right">{next_link}</div>
  </div>
</nav>

<script>
function navigateTo(url) {{
  document.body.classList.add('fade-out');
  setTimeout(function() {{ window.location.href = url; }}, 300);
}}
document.addEventListener('keydown', function(e) {{
{prev_js}
{next_js}
}});
</script>
</body>
</html>
"""
    (OUT / fname).write_text(html, encoding='utf-8')
    return fname

# 슬라이드 생성
written = []
for entry in SLIDES:
    fname = render_slide(*entry)
    written.append((entry[0], entry[1], entry[2], fname))

# index.html
def render_index():
    cards = []
    for num, slug, title, eyebrow, body, extra_css in SLIDES:
        clean_title = title.replace('<br>', ' ')
        fname = f"{num:02d}-{slug}.html"
        cards.append(f"""    <a class="card" href="{fname}" onclick="event.preventDefault(); navigateTo(this.href)">
      <span class="card-num">{num:02d}</span>
      <span class="card-title">{clean_title}</span>
      <span class="card-file">{fname}</span>
    </a>""")
    cards_html = "\n".join(cards)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>v2/1강 — AI에게 일을 시켜보다 — 비주얼 자료</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: #0a0f1a;
  font-family: 'Noto Sans KR', sans-serif;
  color: #e6edf3;
  min-height: 100vh;
  display: flex; justify-content: center;
  padding: 60px 0 80px;
}}
.container {{ width: 1280px; padding: 0 80px; }}
.page-title {{
  font-size: 42px; font-weight: 900;
  background: linear-gradient(135deg, #7c3aed, #38bdf8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  text-align: center; margin-bottom: 10px;
}}
.page-subtitle {{ text-align: center; font-size: 16px; color: #8b949e; margin-bottom: 50px; }}
.grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }}
.card {{
  display: flex; flex-direction: column; gap: 6px; padding: 18px 20px;
  background: rgba(139,148,158,0.04);
  border: 1px solid rgba(139,148,158,0.1);
  border-radius: 12px; text-decoration: none;
  transition: all 0.25s ease;
}}
.card:hover {{
  transform: translateY(-3px);
  border-color: rgba(139,148,158,0.25);
  box-shadow: 0 8px 32px rgba(139, 148, 158, 0.12);
}}
.card .card-num {{ font-size: 28px; font-weight: 900; color: #c9d1d9; }}
.card .card-title {{ font-size: 14px; font-weight: 700; color: #c9d1d9; line-height: 1.4; }}
.card .card-file {{ font-size: 11px; color: #484f58; font-family: 'Courier New', monospace; }}
body {{ opacity: 0; animation: fadeIn 0.4s ease forwards; }}
body.fade-out {{ animation: fadeOut 0.3s ease forwards; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes fadeOut {{ from {{ opacity: 1; transform: translateY(0); }} to {{ opacity: 0; transform: translateY(-12px); }} }}
</style>
</head>
<body>
<div class="container">
  <h1 class="page-title">v2/1강 — AI에게 일을 시켜보다</h1>
  <p class="page-subtitle">전체 {TOTAL}개 슬라이드 · 워크숍 130분 · 클릭 또는 ←/→ 키로 이동</p>
  <div class="grid">
{cards_html}
  </div>
</div>
<script>
function navigateTo(url) {{
  document.body.classList.add('fade-out');
  setTimeout(function() {{ window.location.href = url; }}, 300);
}}
</script>
</body>
</html>
"""
    (OUT / "index.html").write_text(html, encoding='utf-8')

render_index()

# 결과 보고
print(f"✓ {len(written)} slides + index.html written to {OUT}")
for num, slug, title, fname in written:
    print(f"  {num:02d}  {fname}")
