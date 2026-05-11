"""v2/2강 HTML 슬라이드 32장 + index 생성기.
script.md의 [데모: NN-xxx.html] 마커와 1:1 매칭.
v2/1강 디자인 시스템(다크 #0a0f1a · 보라→하늘 그라디언트 · Noto Sans KR) 그대로 차용.
"""
from pathlib import Path

OUT = Path(__file__).parent
TOTAL = 30

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

/* 프롬프트 박스 */
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

/* 카드 그리드 */
.card-grid { display: grid; gap: 16px; width: 100%; max-width: 1100px; }
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
.three-circles { position: relative; width: 520px; height: 380px; display: flex; align-items: center; justify-content: center; }
.circle {
  position: absolute; border-radius: 50%; border: 2px solid;
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-family: 'Noto Sans KR', sans-serif;
}
.circle-outer { width: 380px; height: 380px; border-color: #38bdf8; background: rgba(56, 189, 248, 0.04); color: #38bdf8; font-size: 18px; align-items: flex-start; padding-top: 18px; }
.circle-mid { width: 240px; height: 240px; border-color: #a78bfa; background: rgba(167, 139, 250, 0.06); color: #a78bfa; font-size: 16px; align-items: flex-start; padding-top: 16px; }
.circle-inner { width: 120px; height: 120px; border-color: #ec4899; background: rgba(236, 72, 153, 0.10); color: #f9a8d4; font-size: 14px; }

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
SLIDES = []

def add(num, slug, title, eyebrow, body, extra_css=""):
    SLIDES.append((num, slug, title, eyebrow, body, extra_css))

# --- 01 cover ---
add(1, "cover", "Claude Code를<br>직접 마스터한다", None, """
<div class="kicker-big">VIBE CODING · 2강 (v2)</div>
<p class="cover-sub">어제 가르친 그 도구를 — *직접* 손에 잡는다</p>
<div class="tags">
  
  <span class="tag">함께 입력 <strong>3회</strong></span>
  <span class="tag">v2.1.x 기준</span>
</div>
""", """
.title { font-size: 64px; line-height: 1.2; margin-bottom: 22px; }
.kicker-big { font-size: 16px; font-weight: 700; letter-spacing: 8px; color: #8b949e; margin-bottom: 22px; text-transform: uppercase; }
.cover-sub { font-size: 22px; color: #c9d1d9; text-align: center; margin-bottom: 50px; font-weight: 300; line-height: 1.6; }
""")

# --- 02 recap-circles ---
add(2, "recap-circles", "1강 회수 — 동심원 한 장", "0부 · 도입",
"""<div class="three-circles">
  <div class="circle circle-outer">하니스</div>
  <div class="circle circle-mid">컨텍스트</div>
  <div class="circle circle-inner">프롬프트</div>
</div>
<p class="note" style="font-size:17px;"><strong style="color:#f9a8d4">프롬프트</strong> ⊂ <strong style="color:#a78bfa">컨텍스트</strong> ⊂ <strong style="color:#38bdf8">하니스</strong> &nbsp;·&nbsp; 셋이 *항상 동시에* 박혀있다.</p>
<div class="callout">오늘 그 셋이 *살아있는 도구* — <strong>Claude Code 자체</strong>를 직접 마스터합니다.</div>
""")

# --- 03 promise ---
add(3, "promise", "오늘의 흐름 — Claude Code를 직접 다뤄봅니다", None,
"""<p class="subtitle">1강에서 본 동심원 세 층이 *모두 박혀있는* 한 도구. 명령어와 단축키부터 시작해서, 컨텍스트 관리, 일하는 흐름, 그리고 자동화까지 — 하나씩 손에 잡아봅니다.</p>
""")

# --- 04 claude-md-hierarchy ---
add(4,"claude-md-hierarchy", "CLAUDE.md — 5단계 계층", None,
"""<div class="code-box">Enterprise         조직 정책        <span class="dim">회사 사훈 — 사용자가 끌 수 없음</span>
~/.claude/         User (글로벌)    <span class="dim">내 모든 프로젝트 공통</span>
프로젝트 루트       Project          <span class="dim">팀 위키 — 레포에 커밋</span>
CLAUDE.local       Local            <span class="dim">내 책상 메모 — .gitignore</span>
서브폴더            Subdirectory     <span class="dim">해당 폴더 작업 시에만 lazy load</span></div>
<div class="callout">위에서 아래로 갈수록 <strong>더 구체적</strong>. 더 구체적인 쪽이 우선되도록 설계됨.<br>단, CLAUDE.md는 강제 설정이 아니라 컨텍스트라서 — 100% 일관되게 따르진 않을 수 있음.</div>
""")

# --- 04 claude-md-import ---
add(5,"claude-md-import", "@import — 분리, 그러나 lazy 아님", None,
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">Before — 모든 내용 직접</span>
    <div class="comp-body" style="font-family:'Courier New',monospace; font-size:12px;"># CLAUDE.md<br>## API 엔드포인트<br>- POST /api/login ...<br>- POST /api/register ...<br>... (50개 더)<br><br>→ 200줄 훌쩍 넘김</div>
  </div>
  <div class="comp-arrow">→</div>
  <div class="comp-side comp-new">
    <span class="comp-label">After — 참조만</span>
    <div class="comp-body" style="font-family:'Courier New',monospace; font-size:12px;"># CLAUDE.md<br>## 프로젝트 문서<br>- API 스펙:  <code>@docs/api-spec.md</code><br>- DB 스키마: <code>@docs/db-schema.md</code><br>- 인증 설계: <code>@docs/auth.md</code></div>
  </div>
</div>
<div class="callout"><strong>중요한 진실</strong> — @import는 <strong>lazy load 아님</strong>. 시작 시 5단계 재귀로 모두 로드. 분리는 관리 편의용이지 토큰 절약 아님.</div>
<p class="note">진짜 lazy load는 <strong>Subdirectory CLAUDE.md</strong> (폴더 진입 시) + <strong>Skills</strong> (호출 시).</p>
""")

# --- 05 init-live ---
add(6,"init-live", "/init으로 CLAUDE.md 만들기", None,
"""<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #1 — 모두 자기 폴더에서</div>
  <div><span class="prompt-arrow">&gt;</span> /init</div>
</div>
<div class="code-box">Claude가 자동 분석 →

  ✓ 폴더 구조      (어떤 폴더에 무엇이)
  ✓ 기술 스택      (package.json · requirements.txt)
  ✓ Build/Test     (scripts 필드)
  ✓ README 기반    프로젝트 요약

→ CLAUDE.md 초안 30~80줄로 생성 (200줄 안전권)</div>
<p class="note"><strong>관찰 포인트</strong>: 내가 직접 적으면 빼먹었을 항목이 있나? AI에게 시키면 안 될 일은 자동으로 안 잡힘 — 사람이 채워야.</p>
""")

# --- 06 critical-pattern ---
add(7,"critical-pattern", "200줄 룰 + CRITICAL 패턴", None,
"""<div class="code-box">## 아키텍처 규칙
- <span class="hl">CRITICAL:</span> 모든 API 로직은 app/api/ 라우트 핸들러에서만
- <span class="hl">CRITICAL:</span> secrets는 .env에만 — 코드에 하드코딩 절대 금지

## 개발 프로세스
- <span class="hl">IMPORTANT:</span> 새 기능은 테스트 먼저 작성 (TDD)</div>
<div class="callout">모델은 <strong>영어 대문자</strong>를 강조 신호로 가중치 더 둠. Anthropic 공식 가이드도 권장.</div>
<div class="code-box">키워드        강도    용도
CRITICAL:    최상    위반 시 프로젝트 무너짐 (보안·데이터 무결성)
IMPORTANT:   상      어기면 품질·일관성 손상
NEVER        상      "절대 하지 말 것"
ALWAYS       중상    "항상 따를 것"</div>
""")

# --- 07 plan-mode ---
add(8,"plan-mode", "Plan Mode — 도면 먼저", None,
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">Before — 즉시 실행</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"사용자 인증 기능 만들어줘"<br><br>→ AI가 갑자기 8개 파일 만지기<br>→ 3번째 파일에서 방향 어긋남<br>→ 처음부터 다시 (토큰·시간 낭비)</div>
  </div>
  <div class="comp-arrow">→</div>
  <div class="comp-side comp-new">
    <span class="comp-label">After — /plan</span>
    <div class="comp-body" style="font-family:'Courier New',monospace;">"/plan 사용자 인증 기능 만들어줘"<br><br>→ AI가 계획만 제시<br>&nbsp;&nbsp;1. DB 스키마<br>&nbsp;&nbsp;2. API 3개<br>&nbsp;&nbsp;3. 프론트 1개<br>→ 청중이 읽고 수정 후 실행</div>
  </div>
</div>
<div class="callout">집 짓기 — 망치 들고 바로 못부터 vs 도면을 그리고 시작.<br>Anthropic 공식 4단계: Explore → <strong>Plan</strong> → Code → Verify</div>
""")

# --- 08 four-modes ---
add(9,"four-modes", "모드 4종 — 언제 어느 모드", None,
"""<div class="code-box">┌────────────────────────────┬──────────────────────────────────┐
│ Normal       (<span class="hl">default</span>)        │ 매 작업 전 묻기 (기본값)          │
│ Auto-Accept  (<span class="hl">acceptEdits</span>) ⏵⏵ │ 파일 편집 + 안전한 bash 자동      │
│ Plan         (<span class="hl">plan</span>) ⏸         │ 읽기 전용, 계획만 세움            │
│ Auto         (<span class="hl">auto</span>)           │ AI 분류기가 매 호출 안전성 판단    │
└────────────────────────────┴──────────────────────────────────┘

Auto Mode 사용 조건 (일부 청중은 화면에 안 보일 수 있음)
  플랜      Max / Team / Enterprise / API  ← Pro 불가
  모델      Sonnet 4.6 · Opus 4.6 · Opus 4.7
  Provider  Anthropic API 전용 (Bedrock/Vertex 불가)
  버전      v2.1.83+</div>
<p class="note">한 사례 — 이 레포 작업 중 <code>git push origin main</code> → 분류기가 기본 브랜치 보호 사유로 차단. AI가 내 명령을 거절할 수도 있다는 첫 체감.</p>
""")

# --- 12 part1-summary ---
add(10,"part1-summary", "1부 정리 — 세 줄", "1-6 · 1부 마무리",
"""<div class="card-grid card-grid-3">
  <div class="card accent"><span class="card-num">한 모드</span><span class="card-title">Plan Mode</span><span class="card-body">Shift+Tab × 2 또는 /plan</span></div>
  <div class="card accent"><span class="card-num">한 파일</span><span class="card-title">CLAUDE.md</span><span class="card-body">200줄, CRITICAL, @import</span></div>
  <div class="card accent"><span class="card-num">한 안전망</span><span class="card-title">3 명령</span><span class="card-body">/sandbox · /permissions · /rewind</span></div>
</div>
<p class="note">더 깊이는 <strong>docs/tools/Claude-Code-퍼미션모드.md · CLAUDE-md.md</strong>.</p>
""")

# --- 13 part2-cover ---
add(11,"part2-cover", "2부 — 실전 사용법", None,
"""<div class="code-box">한 세션 = 한 피처     컨텍스트 4도구       Plan-Code-Verify
TDD 루프 + Hooks       에러 통째로          docs 운영 패턴
                                            다른 AI 교차 검증</div>
""")

# --- 11 one-session-one-feature ---
add(12,"one-session-one-feature", "한 세션 = 한 피처", "2-1 · 운영 원칙",
"""<div class="callout"><strong>1강 회수</strong> — *Lost in the Middle* (컨텍스트 길어지면 가운데가 흐려진다)</div>
<div class="code-box">왜
  여러 기능을 한 세션에 → 컨텍스트 누적
                       → 가운데 흐려짐
                       → 이전 작업 임시 가설이 오염
                       → 80% 넘기면 응답 품질 ↓

실전 워크플로우
  1. Plan Mode에서 전체 작업 설계
  2. 첫 단계만 구현 → 완료
  3. /clear 또는 새 세션
  4. 다음 단계로</div>
<p class="note" style="font-size:17px; color:#a78bfa;">"신선한 컨텍스트가 부풀어진 컨텍스트보다 항상 낫다"</p>
""")

# --- 12 context-tools ---
add(13,"context-tools", "컨텍스트 관리 4도구", "2-2 · 칼날 4개",
"""<div class="code-box"><span class="hl">/context</span>   토큰 사용량을 색상 격자로 시각화
           → 80% 넘으면 다음 셋 중 하나로 행동

<span class="hl">/clear</span>     완전 초기화 (새 작업 시작)
<span class="hl">/compact</span>   대화 압축 (맥락 유지)
           /compact focus on auth module   ← 특정 영역만 보존
<span class="hl">/rewind</span>    시점 단위 되돌리기 (대화 + 코드)
           (별칭: /undo, /checkpoint)</div>
<div class="callout"><strong>한 줄 운영</strong> — 새 피처=<code>/clear</code>, 같은 피처 무거움=<code>/compact</code>, 방향 잘못=<code>/rewind</code>, 매번 모름=<code>/context</code> 먼저</div>
""")

# --- 13 context-live ---
add(14,"context-live", "/context 같이 보기", "2-3 · 함께 입력 #2",
"""<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #2 — 자기 세션 상태 확인</div>
  <div><span class="prompt-arrow">&gt;</span> /context</div>
</div>
<div class="callout">세션 *비어있으면* — 강사가 미리 1강 회수 한 줄 입력하게 함</div>
<p class="note"><strong>관찰 포인트</strong>: <em>시스템 프롬프트</em> 비중 (의외로 큼) · <em>MCP 도구 설명</em> 비중 (안 쓰면 끄기) · <em>CLAUDE.md</em> 비중 (200줄 룰 체감)</p>
""")

# --- 14 explore-plan-code-verify ---
add(15,"explore-plan-code-verify", "Plan-Code-Verify 워크플로우", "2-4 · Anthropic 공식 4단계",
"""<div class="callout"><strong>1강 회수</strong> — 하니스 4축 (도구·반복·검증·기억)이 살아있는 패턴</div>
<div class="card-grid card-grid-4">
  <div class="card accent"><span class="card-num">1</span><span class="card-title">Explore</span><span class="card-body">Plan Mode 안에서 *관련 코드 읽기*<br><code>/agents Explore</code></span></div>
  <div class="card accent"><span class="card-num">2</span><span class="card-title">Plan</span><span class="card-body">구현 계획 작성 → 검토 → 수정<br><code>Ctrl + G</code> 외부 에디터</span></div>
  <div class="card accent"><span class="card-num">3</span><span class="card-title">Code</span><span class="card-body">Auto-Accept 전환해서 실행<br><code>/diff</code> 변경 확인</span></div>
  <div class="card accent"><span class="card-num">4</span><span class="card-title">Verify</span><span class="card-body">테스트·빌드·커밋<br><code>/rewind</code> 안전 되돌리기</span></div>
</div>
""")

# --- 15 tdd-loop ---
add(16,"tdd-loop", "TDD 루프 — 한 입씩 자주", "2-5 · 일상 비유",
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">요리</span>
    <div class="comp-body">재료 손질 → <strong>한 입 맛보기</strong> → 간 조절<br><br>→ 한 입 맛보기 → 간 조절<br><br>→ 다 됐으면 완성</div>
  </div>
  <div class="comp-arrow">≈</div>
  <div class="comp-side comp-new">
    <span class="comp-label">코딩 TDD</span>
    <div class="comp-body">작은 변경 → <strong>테스트 돌리기</strong> → 통과 확인<br><br>→ 다음 변경 → 테스트 → 통과<br><br>→ 다 됐으면 커밋</div>
  </div>
</div>
<p class="note">문제 생겨도 <strong>마지막 커밋</strong>으로 돌아가면 됨. 한 입씩 자주 맛보는 셰프 vs 마지막에 한 번에 — 누가 더 안정적일까.</p>
""")

# --- 16 hooks-teaser ---
add(17,"hooks-teaser", "Hooks 맛보기 — 매번 입력 vs 한 번 박아두기", "2-5 · Hooks 첫 등장",
"""<div class="code-box">Before  매번 입력     "코드 수정 → 테스트 → 린트 → 커밋"   <span class="bad">4줄 반복</span>
After   한 번 박아둠   파일 편집할 때마다 자동 실행          <span class="ok">0줄</span></div>
<div class="callout"><strong>살아있는 사례</strong> — 이 레포의 <code>caveman-kor</code> hook이 모든 응답에 *짧은 한국어로*를 자동 주입 → 출력 토큰 <strong>30~50% 절감</strong></div>
<p class="note">본격 4 이벤트·다른 활용은 <strong>3부 28·29 슬라이드</strong>. 지금은 *"매번 시킬 일을 한 번 박아둘 수 있다"* 까지만.</p>
""")

# --- 17 error-logs ---
add(18,"error-logs", "에러 로그 통째로 + Escape 타이밍", "2-6 · 디버깅 철칙",
"""<div class="compare-2col">
  <div class="comp-side comp-old">
    <span class="comp-label">나쁜 예 — 해석 들어감</span>
    <div class="comp-body" style="font-family:'Courier New',monospace; font-size:12px;">"Python 코드가 NameError 나는데<br>변수가 안 잡히는 것 같아"<br><br>→ AI가 *그 해석*에 끌려감</div>
  </div>
  <div class="comp-arrow">→</div>
  <div class="comp-side comp-new">
    <span class="comp-label">좋은 예 — 통째로</span>
    <div class="comp-body" style="font-family:'Courier New',monospace; font-size:11px;">Traceback (most recent call last):<br>&nbsp;&nbsp;File "main.py", line 47, in &lt;module&gt;<br>&nbsp;&nbsp;&nbsp;&nbsp;result = process(data)<br>NameError: name 'analyzer' is not defined<br><br>→ AI가 *스택 전체*를 자기 시선으로</div>
  </div>
</div>
<div class="callout"><strong>Escape 타이밍</strong> — Claude의 *thinking 로그*에서 잘못된 가정이 보이면 즉시 Escape. 잘못된 가정 위에 쌓이는 코드는 전부 쓸모없음.</div>
""")

# --- 18 docs-folder ---
add(19,"docs-folder", "docs 폴더 운영 — 이 강의 레포가 살아있는 예시", "2-7 · 문서 주도 개발",
"""<div class="code-box">프로젝트 루트/
├── CLAUDE.md                  <span class="dim">(200줄 — 참조만)</span>
└── docs/
    ├── concepts/              <span class="dim">LLM·Transformer·바이브코딩</span>
    ├── techniques/            <span class="dim">프롬프트·컨텍스트·하니스 엔지니어링</span>
    ├── phenomena/             <span class="dim">환각·시코펀시·Lost-in-the-Middle</span>
    ├── tools/                 <span class="dim">Claude Code · MCP · Skills</span>
    └── methodologies/         <span class="dim">워터폴·애자일·하이퍼-워터폴</span></div>
<div class="callout"><strong>일상 비유</strong> — 회사의 *팀 위키*와 *팀 라이브러리*. 위키는 *목차*, 라이브러리는 *전체 문서*. 매번 라이브러리 통째로 외울 필요 없음.</div>
<p class="note"><strong>문서 주도 개발</strong> — 코드 짜기 전에 *문서 먼저*. 결정·설계가 영속, 새 세션·새 동료가 같은 컨텍스트에서 시작. <code>docs/techniques/문서-주도-개발.md</code></p>
""")

# --- 19 cross-llm-review ---
add(20,"cross-llm-review", "다른 AI에게 비평 받기", "2-8 · 교차 검증",
"""<div class="code-box"><span class="hl">/export session.md</span>     파일로 저장
<span class="hl">/export --clipboard</span>    클립보드로
<span class="hl">/copy</span>                   마지막 응답만 복사
<span class="hl">/copy 2</span>                 마지막에서 2번째 응답만

→ 이 텍스트를 ChatGPT나 Gemini에 붙여넣고:

"이 대화를 분석해서, Claude가 놓치고 있는 것이나
 잘못된 접근이 있으면 지적해줘"</div>
<div class="callout"><strong>왜 통하나</strong> — 모델마다 학습 데이터·치우침이 다름. 같은 문제를 *다른 시선*으로 보면 1강에서 본 <em>반대 검증</em> 효과 ×2.</div>
""")

# --- 23 part2-summary ---
add(21,"part2-summary", "2부 정리 — 다섯 원칙", "2-9 · 2부 마무리",
"""<div class="card-grid card-grid-2">
  <div class="card accent"><span class="card-num">1</span><span class="card-title">한 세션 = 한 피처</span></div>
  <div class="card accent"><span class="card-num">2</span><span class="card-title">/context로 *현재 상태* 먼저</span><span class="card-body">80% 넘으면 행동</span></div>
  <div class="card accent"><span class="card-num">3</span><span class="card-title">Plan-Code-Verify 4단계 안에서</span></div>
  <div class="card accent"><span class="card-num">4</span><span class="card-title">테스트는 한 입씩 자주</span></div>
</div>
<div class="callout" style="margin-top:14px;"><strong>5.</strong> 에러는 통째로, 잘못된 가정엔 Escape</div>
""")

# --- 24 part3-cover ---
add(22,"part3-cover", "3부 — 자동화 4부품", None,
"""<p class="subtitle">Skills · Sub-Agent · Hooks · MCP — 1강에서 맛본 부품들의 본격 풀이</p>
<div class="callout">깊이는 <strong>3강</strong>(하니스 세팅)에서.</div>
""")

# --- 22 skills-structure ---
add(23,"skills-structure", "Skills — 업무 매뉴얼", "3-1 · 구조",
"""<div class="code-box">.claude/skills/
└── ppt-generator/                  ← 스킬 폴더
    ├── <span class="hl">SKILL.md</span>                  ← 필수: frontmatter + 지시문
    ├── template.md                 ← 선택: 템플릿
    └── examples/                   ← 선택: 예제

<span class="hl">2단계 lazy loading</span>
  평소        :  이름 + description만 (~50-100바이트)
  호출 시     :  본문 + 참고 파일 전부 로드</div>
<div class="callout">평소엔 가볍게, 쓸 때만 전체 로드 — <strong>CLAUDE.md(항상 로드)·MCP(항상 로드)와 결정적 차이</strong></div>
<div class="code-box">---
name: ppt-generator
description: "PPT 발표자료 자동 생성.
  'PPT 만들어줘', '발표자료 작성' 요청 시 트리거."
---</div>
""")

# --- 23 skill-live ---
add(24,"skill-live", "사전 작성한 Skill 보여주기", "3-1 · presentation_slides 사례",
"""<div class="callout">라이브 생성은 너무 많은 변수 (플러그인·대화형·파일 시스템·권한). 비개발자 진입 위험. <strong>진행자 사전 작성한 작은 skill 한 장</strong>을 화면으로.</div>
<div class="code-box">.claude/skills/presentation_slides/
└── SKILL.md
    ├── frontmatter (name, description)
    ├── 디자인 시스템 안내 (다크 테마·보라→하늘 그라디언트)
    ├── HTML 보일러플레이트
    └── 절차 (입력 수집 → 슬라이드 목록 확정 → 생성)

호출:  > <span class="hl">/presentation_slides</span></div>
<div class="prompt-box">
  <div class="prompt-tag">함께 입력 #3 — 선택</div>
  <div><span class="prompt-arrow">&gt;</span> /skills    <span style="color:#6e7681;">  ← 자기 PC의 skill 목록 확인</span></div>
</div>
<p class="note">빈 청중도 <em>"내 PC엔 아직 없구나, 만들면 되겠네"</em> 까지만. 라이브 *생성*은 3강에서 본격.</p>
""")

# --- 24 sub-agents ---
add(25,"sub-agents", "Sub-Agent — 회사의 부서", "3-2 · 가장 많이 쓰는 3종",
"""<div class="callout"><strong>1강 회수</strong> — *회사의 부서*. 메인 Claude는 PM, 서브에이전트는 디자인·개발·QA팀</div>
<div class="card-grid card-grid-3">
  <div class="card accent"><span class="card-num">Explore</span><span class="card-title">탐색 전담</span><span class="card-body">Haiku, 빠름<br>"이 코드 어디에 있나?"</span></div>
  <div class="card accent"><span class="card-num">Plan</span><span class="card-title">계획만 세우는 전담</span><span class="card-body">"어떻게 짤지 먼저 보자"</span></div>
  <div class="card accent"><span class="card-num">General-purpose</span><span class="card-title">다단계 작업</span><span class="card-body">탐색하고 고치고 테스트까지</span></div>
</div>
<p class="note">+ 2개 더 — <strong>Bash</strong>(별도 컨텍스트 명령) · <strong>Claude Code Guide</strong>(Q&A). 디테일은 <code>docs/tools/서브에이전트.md</code></p>
<p class="note">언제 — *대량 출력이 메인을 오염시킬 작업* (전체 테스트 로그·47개 파일 검색). <strong>직접 하기 vs 심부름 시키기</strong> 판단.</p>
""")

# --- 25 hooks ---
add(26,"hooks", "Hooks — 자동화 엔진 본격", "3-3 · 이벤트 트리거",
"""<div class="callout"><strong>일상 비유</strong> — 집안의 센서들. 문 열면 불 켜짐 / 차 시동 걸면 안전벨트 경고. <em>이벤트 → 자동 액션</em>.</div>
<div class="code-box">도구 호출 직전     <span class="hl">PreToolUse</span>     "이거 진짜 실행해도 돼?"
도구 실행 직후     <span class="hl">PostToolUse</span>    "끝났네 — 자동으로 lint·포맷"
응답 대기 시       <span class="hl">Notification</span>   "사용자 응답 기다림 — 알림 보내기"
턴 종료 시         <span class="hl">Stop</span>           "작업 끝 — 보고서·상태 저장"
                                  + UserPromptSubmit · SessionStart 등 다수</div>
<p class="note"><strong>주의</strong> — Hook 실행 중 Claude는 *멈춰서 기다림*. timeout 꼭 설정, 무거운 작업은 백그라운드(<code>&amp;</code>)로.</p>
""")

# --- 26 hooks-before-after ---
add(27,"hooks-before-after", "Hooks 살아있는 사례 — caveman-kor", "3-3 · 실제 사용",
"""<div class="code-box">caveman-kor        UserPromptSubmit 이벤트에 박힌 hook
                   기능: 모든 prompt 직후 자동으로 한 줄 주입
                        — "짧고 한국어로, 군더더기 빼고 답해라"
                   위치: <span class="hl">~/.claude/settings.json</span>

결과 (지난 6개월 실측)
    출력 토큰        <span class="ok">30~50% 감소</span>
    응답 속도        체감 30% 빠름
    설치 비용        settings.json 한 블록 (5~10줄)</div>
<div class="callout"><strong>비유</strong> — 회사의 *기본 안내문*. 신입에게 매번 안 말하고 *팀 가이드*에 박아두면 자동. Hook은 그 *팀 가이드*를 Claude Code 안에서 자동 들이미는 장치.</div>
<p class="note">1강에서 본 *하니스 = 모델 주변 환경 전체*의 <strong>가장 작은 단위 사례</strong>. 매일 신경 쓸 일을 *한 줄로 박는다*.</p>
""")

# --- 27 mcp-decision ---
add(28,"mcp-decision", "MCP + 결정표 — 언제 무엇을 쓰나", "3-4 · 마지막 부품",
"""<div class="callout"><strong>MCP</strong> = AI 통합의 USB-C. Anthropic 2024-11 공개 → 2025-12 Linux Foundation 기증 → Kubernetes·PyTorch와 같은 *중립 인프라*로 격상</div>
<div class="code-box">상황                                  쓸 도구
─────────────────────────────────────────────────
프로젝트 *전체*에 항상 적용할 규칙       →  <span class="hl">CLAUDE.md</span> (200줄 룰북)
이 폴더 안 작업에만 적용할 규칙          →  <span class="hl">Subdirectory CLAUDE.md</span> (lazy)
자주 반복하는 *절차·작업 묶음*           →  <span class="hl">Skills</span> (lazy, /이름)
이벤트마다 자동 실행 (lint·알림·차단)    →  <span class="hl">Hooks</span> (settings.json)
외부 서비스 연결 (GitHub·Figma·DB)       →  <span class="hl">MCP</span>
대량 출력·격리된 분석                    →  <span class="hl">Sub-Agent</span> (/agents)</div>
<p class="note">"매번 직접 시키지 않고 어디에 박을까" 결정 시 — <strong>이 표 한 장만</strong>.</p>
""")

# --- 28 summary ---
add(29,"summary", "오늘의 압축 — 한 장", "4-1 · 책상 옆에 붙이세요",
"""<div class="code-box">1부 기본기      Plan Mode (Shift+Tab × 2)
                CLAUDE.md (200줄, CRITICAL, @import)
                안전망 (/sandbox · /permissions · /rewind)

2부 실전        한 세션 = 한 피처
                컨텍스트 4도구 (/context · /clear · /compact · /rewind)
                Plan-Code-Verify 4단계
                에러는 통째로, 잘못된 가정엔 Escape
                docs/ 폴더로 *문서 주도 개발*

3부 자동화      Skills (재사용 워크플로우, /skills)
                Sub-Agent (5종 내장, /agents)
                Hooks (4 이벤트 + 그 외 다수, /hooks)
                MCP (USB-C, /mcp)</div>
<div class="callout">이 한 장이 <strong>오늘의 압축</strong>. 인쇄해서 책상 옆에 붙여두세요.</div>
""")

# --- 29 next-lecture ---
add(30,"next-lecture", "다음 강의 — 3강 예고", "4-2 · 마무리",
"""<p class="subtitle">오늘 *도구 자체*를 마스터했어요. 다음 시간은 그 도구를 <strong>내 프로젝트 위에 진짜로 한 층 올리는 법</strong>.</p>
<div class="code-box">3강 — 하니스 세팅

내 프로젝트에 2층 한 층 더 올리기 — 4종 markdown만 손봐도 충분

  CLAUDE.md          이 프로젝트의 룰북
  docs/              PRD · ADR · UI_GUIDE 4종
  skills/            /harness · /review 같은 재사용 워크플로우
  hooks/             caveman-kor 같은 출력 토큰 절감 hook

클라이맥스 — claude -p (CI/CD에 헤드리스 Claude 끼우기)

그리고 4강 — Dicom Viewer 만들기 (5단계 워크플로우 라이브)</div>
<p class="note" style="margin-top:24px; color:#c9d1d9; font-size:18px;">오늘 강의 끝. 감사합니다.</p>
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
<title>{title.replace('<br>', ' ')} — v2/2강</title>
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
<title>v2/2강 — Claude Code를 직접 마스터한다 — 비주얼 자료</title>
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
  <h1 class="page-title">v2/2강 — Claude Code를 직접 마스터한다</h1>
  <p class="page-subtitle">전체 {TOTAL}개 슬라이드 · 클릭 또는 ←/→ 키로 이동</p>
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

print(f"✓ {len(written)} slides + index.html written to {OUT}")
for num, slug, title, fname in written:
    print(f"  {num:02d}  {fname}")
