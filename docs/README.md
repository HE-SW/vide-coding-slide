# 바이브코딩 강의 지식 베이스

비개발자 대상 바이브코딩 강의용 레퍼런스 문서 모음. 강의자가 청중에게 정확한 출처와 함께 개념을 전달할 수 있도록, 모든 문서는 다음 3-조건 서사를 따른다.

1. **왜 이렇게 부르나** — 이름의 유래 (인물·연도·어원)
2. **그전에는 어떤 문제가 있었나** — 등장 직전의 한계
3. **어떻게 해결했나** — 이 개념이 가져온 변화

---

## 카테고리

### `concepts/` — 큰 개념
사람이 만든 패러다임/모델 종류. 한 시대를 가르는 분기점이 되는 단어들.

- [바이브코딩 (Vibe Coding)](concepts/바이브코딩.md) — 2025년 2월, 코드가 아니라 분위기로 만드는 새 흐름
- [LLM (Large Language Model)](concepts/LLM.md) — 다음 단어를 예측하는 초거대 AI
- [Transformer](concepts/Transformer.md) — 모든 LLM의 뼈대가 된 2017년 신경망 구조
- [Tokenization (토큰화)](concepts/Tokenization.md) — LLM이 글자를 단어 덩어리로 보는 방식. strawberry R 문제의 정체
- [Tool Use (도구 사용·함수 호출)](concepts/Tool-Use.md) — LLM이 *말만 하지 않고 행동하는* 능력. ChatGPT의 function calling, Claude의 tool use
- [Human-in-the-Loop (HITL)](concepts/Human-in-the-Loop.md) — 자동화 흐름의 결정적 체크포인트에서 사람이 승인·거부·수정. 3-tier 모델 + LangGraph `interrupt()` 표준
- [AI Adoption Spectrum (성숙도 4단계)](concepts/AI-Adoption-Spectrum.md) — AI-aware → AI-enabled → AI-native → AI-maximalist. 청중 자기 진단 도구
- [Agentic Engineering](concepts/Agentic-Engineering.md) — 바이브코딩의 *2026 진화형*. Karpathy 2026-05 Sequoia AI Ascent 선언. PEV(Plan-Execute-Verify) loop + Spec-driven development

### `techniques/` — 기법
실무에서 적용하는 방법론. "어떻게" 잘 쓰는가에 대한 답. 3가지 엔지니어링은 *허브* + *세부 sub-files*로 구성.

#### 부모 (인덱스 허브)
- [프롬프트 엔지니어링 (Prompt Engineering)](techniques/프롬프트-엔지니어링.md) — 무엇을 요청할 것인가 + 5가지 패턴 군 인덱스
- [컨텍스트 엔지니어링 (Context Engineering)](techniques/컨텍스트-엔지니어링.md) — 어떤 정보를 함께 줄 것인가 + 4 레이어 인덱스
- [하니스 엔지니어링 (Harness Engineering)](techniques/하니스-엔지니어링.md) — 어떻게 반복적으로 검증할 것인가 + 5 구성 요소 인덱스

#### 컨텍스트 엔지니어링 4 레이어 (`techniques/context/`)
- [System Context](techniques/context/system-context.md) — 역할·규칙·톤 (가장 안쪽 *틀*)
- [Conversation Context](techniques/context/conversation-context.md) — 사용자 입력 + 대화 + 메모리(단·장기)
- [Knowledge Context](techniques/context/knowledge-context.md) — RAG·외부 문서·웹 검색
- [Tool & Environment Context](techniques/context/tool-environment-context.md) — 도구 결과 + 시각·OS·디렉토리

#### 프롬프트 엔지니어링 5 패턴 (`techniques/prompt/`)
- [Zero/One/Few-shot](techniques/prompt/zero-few-shot.md) — 예시 0~5개
- [Chain-of-Thought · ToT · GoT](techniques/prompt/chain-of-thought.md) — 단계별 추론
- [Role Prompting](techniques/prompt/role-prompting.md) — 역할 부여 (한계 포함)
- [Self-Consistency · Multi-Sampling](techniques/prompt/self-consistency.md) — 다중 샘플링 다수결
- [Meta-Prompting · Chaining · ReAct](techniques/prompt/meta-prompting.md) — 프롬프트의 *흐름*

#### 하니스 엔지니어링 5 구성 요소 (`techniques/harness/`)
- [Tools](techniques/harness/tools.md) — 모델의 *손*
- [Subagents & Delegation](techniques/harness/subagents-and-delegation.md) — 분업·위임
- [Evaluation Loop](techniques/harness/evaluation-loop.md) — Anthropic 3-agent 검증
- [Control & State](techniques/harness/control-and-state.md) — Phase 분할 + docs 영속화
- [Permissions & Hooks](techniques/harness/permissions-and-hooks.md) — 결정론적 안전장치

#### 부속 기법
- [RAG (Retrieval-Augmented Generation)](techniques/RAG.md) — Knowledge context 의 표준 구현
- [문서 주도 개발 (PRD·ARCHITECTURE·ADR·UI_GUIDE)](techniques/문서-주도-개발.md) — AI에게 *프로젝트 전체*를 알려주는 4종 문서 패턴
- [TDD (Test-Driven Development)](techniques/TDD.md) — Kent Beck의 *테스트 먼저* 규율. AI 시대 자동 검증 게이트의 토대. `CLAUDE.md` 템플릿의 `CRITICAL:` 항목 핵심
- [Orchestration (오케스트레이션)](techniques/Orchestration.md) — 4대 프레임워크 (LangGraph·Claude Agent SDK·OpenAI Agents SDK·Strands) + 4 패턴 (Orchestrator-Worker / Sequential / Parallel / Evaluator-Optimizer) + Anthropic 2026-05 *dreaming*·20-parallel

### `phenomena/` — 현상/한계
관찰되는 문제. 강의에서 "주의할 점"으로 짚어야 할 항목들.

- [환각 (Hallucination)](phenomena/환각.md) — LLM이 그럴듯하게 지어내는 거짓말
- [Sycophancy (아부)](phenomena/Sycophancy.md) — "이거 틀리지 않아?" 한 마디에 답을 뒤집는 현상
- [비결정성 (Non-Determinism)](phenomena/비결정성.md) — 같은 질문에 매번 다른 답이 나오는 이유
- [Knowledge Cutoff (지식 컷오프)](phenomena/Knowledge-Cutoff.md) — AI가 어제 일을 모르는 이유
- [Lost in the Middle](phenomena/Lost-in-the-Middle.md) — 컨텍스트 가운데를 LLM이 무시하는 위치 편향

### `people/` — 인물·회사
강의에서 인용하거나 맥락 설명에 필요한 인물·조직.

- [Andrej Karpathy](people/Andrej-Karpathy.md) — "바이브코딩"·"컨텍스트 엔지니어링" 두 용어를 정착시킨 인물
- [Anthropic](people/Anthropic.md) — Claude·Claude Code·MCP를 만든 회사. 2021년 OpenAI 출신 7인이 *AI 안전*을 출발점으로 창립. (회사 항목이 늘면 `companies/` 신설 검토)

### `tools/` — 도구·제품
강의에서 시연하거나 청중이 실제로 써볼 도구의 사용 레퍼런스.

- [Claude Code](tools/Claude-Code.md) — Anthropic 공식 CLI. 슬래시 명령어 정리
- [Claude Code 입력 문법](tools/Claude-Code-입력문법.md) — `!`(셸 즉시 실행) · `@`(파일 mention) · `/`(슬래시) · `#`(deprecated) + ESC 두 번·`Ctrl+R`·`Shift+Tab` 등 키보드 단축키
- [Claude Code 세션 운영](tools/Claude-Code-세션운영.md) — 컨텍스트 오염·세션 분리 6가지 도구 (`/clear` `/compact` `/btw` `/branch` 서브에이전트 worktree)
- [왜 CLI인가](tools/CLI를-쓰는-이유.md) — claude.ai 채팅 vs Claude Code, 비개발자 청중을 위한 비교
- [CLAUDE.md](tools/CLAUDE-md.md) — Claude Code가 자동으로 읽는 프로젝트 메모리 파일 (4계층 메모리 + `@path` import)
- [Claude Code 1층 하니스](tools/Claude-Code-1층-하니스.md) — 시스템 프롬프트·권한 체크·도구 경계·JSON 스키마 4가지 *내장* 안전장치
- [Claude Code 시스템 프롬프트](tools/Claude-Code-시스템프롬프트.md) — 1층 #1 요소 deep dive. 2025·2026 두 차례 유출 사건 정리
- [Claude Code Hooks](tools/Claude-Code-Hooks.md) — 12개 라이프사이클 이벤트 + exit code 0/2 동작 + `caveman-kor` 사례
- [Claude Code Skills](tools/Claude-Code-Skills.md) — `/이름` 한 줄 호출. SKILL.md frontmatter, `~/.claude/skills/` vs `.claude/skills/`
- [Claude Code Plugin](tools/Claude-Code-Plugin.md) — Skills + Hooks + MCP + Agent 묶음. `/plugin install`. 공식 마켓플레이스 100+개
- [Plugin Marketplace](tools/Plugin-Marketplace.md) — 플러그인을 *어디서 찾고 어떻게 등록하는가*. `/plugin marketplace add`, 공식·커뮤니티·사내 사설 카탈로그 지도
- [Claude Code 퍼미션 모드](tools/Claude-Code-퍼미션모드.md) — plan / default / acceptEdits / auto / bypassPermissions + dontAsk
- [Claude Code 헤드리스 모드 (`claude -p`)](tools/Claude-Code-Headless-모드.md) — 자동화 핵심 매커니즘. `execute.py`가 5단계를 사람 없이 흘리는 이유
- [MCP (Model Context Protocol)](tools/MCP.md) — AI ↔ 외부 도구 연결의 *USB-C*. 3 primitives (tools/resources/prompts), 2 transports (stdio/HTTP). 2025-12 Linux Foundation 기증
- [서브에이전트 (Subagent)](tools/서브에이전트.md) — 큰 작업을 *전문 분야 작은 AI 동료*에게 위임. YAML frontmatter, 모델 라우팅
- [oh-my-claudecode (OMC)](tools/oh-my-claudecode.md) — Claude Code 위에 얹는 멀티 에이전트 오케스트레이션 플러그인 (MIT)
- [andrej-karpathy-skills](tools/andrej-karpathy-skills.md) — Karpathy의 LLM 4대 실패 패턴을 65줄 CLAUDE.md로 압축한 행동 가이드 (MIT)

### `rules/` — 프로젝트 행동 규율 (실제 적용 파일)
이 레포 자체에 적용하는 코딩 규율. 강의 시연 자료로도 사용된다.

- [coding-guidelines.md](rules/coding-guidelines.md) — Karpathy 4원칙(Think · Simple · Surgical · Goal-Driven)을 한국어 강의톤으로 옮긴 행동 가이드라인. *"한 장의 행동 규율을 어떻게 까는가"* 슬라이드 시연용.

### `methodologies/` — 개발 방법론
바이브코딩의 위치를 이해하기 위해 알아야 할 전·후 방법론.

- [워터폴 (Waterfall)](methodologies/워터폴.md) — 1970년 등장, 단계별 한 방향 흐름. 규율은 강하나 느림.
- [애자일 (Agile)](methodologies/애자일.md) — 2001년 선언. 속도는 얻었으나 문서·규율 손실.
- [하이퍼-워터폴 (Hyper-Waterfall)](methodologies/하이퍼-워터폴.md) — 2026년 edwardkim. AI 시대에 둘 다 가지려는 1인+AI 방법론.

### `live-demos/` — 강의 운영 메모 (회차별)
청중이 자기 PC에 *동시에 입력*하는 prompt 묶음 + 예상 출력 + fallback. 다른 docs와 달리 *회차 단위로 묶인* 운영 메모(예외 카테고리).

- [v2-1강](live-demos/v2-1강.md) — v2 워크숍(130분, 비개발자 외부)용 함께 입력 prompt 6개 + 라이브 라운드. 1차 발표 피드백(예시 부족) 보강판.
- [v2-2강](live-demos/v2-2강.md) — v2 강의(90분, 비개발자 — Claude Code 자체)용 함께 입력 prompt 3개 (/init · /context · skill-creator).
- [army-1강](live-demos/army-1강.md) · [army-2강](live-demos/army-2강.md) · [army-3강](live-demos/army-3강.md) — army 평행 트리 1차 운영 메모.

---

## 사용 방법

- 강의 준비 시 각 강의 폴더의 `script.md` 섹션과 이 문서를 교차 확인
- 즉석 질문 대비: 각 문서 하단 **출처** 섹션에 1차/2차 자료 URL 정리
- 새 개념이 발견되면 적절한 카테고리에 추가 (필요 시 새 카테고리 신설)
- 새 문서 작성 규칙은 [docs/CLAUDE.md](CLAUDE.md) 참조 — 3-조건 서사·예시 4종·데이터 신선도·체크리스트
- **회차 번호·슬라이드 번호 의존 금지** — docs는 강의 스크립트가 재작성돼도 깨지지 않게 자족적으로 작성한다 ([docs/CLAUDE.md §6](CLAUDE.md))
