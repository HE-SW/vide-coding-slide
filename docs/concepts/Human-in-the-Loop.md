# Human-in-the-Loop (HITL, 사람이 루프 안에)

> 자동화·AI 흐름의 *결정적 체크포인트*에서 **사람이 승인·거부·수정**하는 패턴. *완전 자율*과 *전부 수동* 사이의 중간 지대. 강의의 *"사람이 마지막 결정한다"* 메시지의 정식 이름.

## 1. 왜 "Human-in-the-Loop"이라고 부르나

- **Human + In + The + Loop**. *"제어 루프 *안에* 사람이 들어 있다"* 라는 뜻. 전통 자동제어 이론(1950s~)의 표현이 AI 시대로 확장.
- **2010년대** — 머신러닝의 *데이터 라벨링*에서 사람의 개입(라벨 검수·교정)을 가리키는 용어로 정착.
- **2024~2025** — Agent 시대 들어 *"AI가 행동하기 전에 사람이 확인"* 으로 의미 확장.
- **2026 표준 매커니즘**: **LangGraph 의 `interrupt()` 함수**. 그래프 노드에서 일시정지 + 상태 보존 + 사람 응답 후 재개.

## 2. 그전에는 어떤 문제가 있었나

AI 에이전트 시대 들어 두 극단의 위험이 드러났다:

- **완전 자율** — 사람 개입 0. *되돌릴 수 없는 사고* 위험. 결제·법적 합의·프로덕션 인프라 변경에 부적합.
- **전부 수동** — 매 행동에 확인. *느림·사용자 피로·유효 자동화 0*. 200번 다이얼로그에 막혀 5분 작업이 1시간.

→ *위험도에 따른 차등 개입* 매커니즘이 필요했다.

**일상 비유**: 자율주행차가 *고속도로*에서는 자율, *주차장 끼어들기*에서는 사람 개입. 같은 차가 상황에 따라 *다른 자율 수준*. HITL 이 정확히 그 *상황별 차등*.

## 3. 어떻게 해결했나 — 3-Tier 모델

```text
   더 자율 ←──────────────────────────────────→ 더 안전
   ┌──────────┐    ┌────────────────┐    ┌─────────────────┐
   │ No HITL  │    │ Review After   │    │ Approve Before  │
   │ (자율)   │    │ (비동기 검토)   │    │ (동기 승인)      │
   └──────────┘    └────────────────┘    └─────────────────┘
   읽기·검색       콘텐츠 생성 (블로그)   결제·삭제·이메일 발송
   데이터 분석     리포트 작성           프로덕션 배포
                                         되돌릴 수 없는 작업
```

| 위험 수준 | 패턴 | 예시 |
|---|---|---|
| 저 (읽기·정보 수집) | **No HITL** | grep, 웹 검색, 데이터 분석 |
| 중 (생성, 되돌릴 수 있음) | **Review After** (async) | 블로그 초안, 코드 PR, 리포트 |
| 고 (되돌릴 수 없음) | **Approve Before** (sync) | 결제 실행, 이메일 발송, 프로덕션 배포 |

### 사람 응답의 4가지 옵션

```text
사람이 받는 인터럽트:
  1. Approve     "OK, 그대로 실행"
  2. Edit        "이렇게 수정해서 실행"
  3. Reject      "하지 마. 이유: ..."
  4. Respond     "모델에게 답변/추가 정보 제공"
```

## HITL vs HOTL — 헷갈리는 두 친구

| | **HITL** (Human-in-the-Loop) | **HOTL** (Human-on-the-Loop) |
|---|---|---|
| 사람 위치 | 루프 *안* | 루프 *위* (감독) |
| 매번 승인 | 예 (체크포인트마다) | 아니오 (이상 시만 개입) |
| 비유 | 자전거 핸들 잡기 | CCTV 보다가 이상 시 출동 |
| 적합 | 고위험·되돌릴 수 없는 작업 | 대규모 자동화 운영 |

→ 두 패턴은 *대체*가 아니라 *상황별 선택*.

## Before / After

```text
[BEFORE — 완전 자율]
USER: "이 PR 머지하고 production 배포해"
AI:   [merge → deploy] (1초 만에)
      → 코드에 결함 있어도 production 까지 흘러감

[AFTER — Approve Before HITL]
USER: "이 PR 머지하고 production 배포해"
AI:   "다음을 실행하려 합니다:
       1) git merge feature-x → main
       2) deploy main → production
       총 12개 파일 변경, 2,341줄 추가
       [Approve / Edit / Reject]"
사람: "Reject — 보안 검토 필요"
AI:   "중단. 보안 검토를 먼저 진행하겠습니다."
```

## 라이브 시연 가능한 예시

### 시연 1 — Claude Code 의 권한 다이얼로그
```bash
> "이 폴더 정리해줘"
[Claude → rm -rf 시도]
[다이얼로그]
  "rm -rf 실행할까요?
   영향: 50개 파일 (config.yaml, src/, tests/, ...)
   되돌릴 수 없습니다.
   [y/n/edit]"
사용자: "n"  → 작업 중단
```
→ 정확히 *Approve Before* HITL 패턴이 작동하는 모습.

### 시연 2 — Plan 모드의 HITL
```bash
[plan 모드 진입 — Shift+Tab Shift+Tab]
> "이 코드베이스 보안 점검하고 고쳐줘"
[Claude] 코드 변경 ❌, 계획서만 출력
        → ExitPlanMode 호출 → 사용자 검토
[사용자] "OK, acceptEdits로 진행"
[Claude] 계획대로 수정 시작
```

## 4. 실제 사례 (2026 기준)

- **Claude Code 퍼미션 시스템** (자세히는 [퍼미션 모드](../tools/Claude-Code-퍼미션모드.md)): 5+1 모드 자체가 HITL 강도 손잡이.
- **LangGraph `interrupt()`** — 47M 월다운로드 기준 표준 매커니즘. 그래프 노드에서 정지·재개.
- **하이퍼-워터폴 5단계** ([하이퍼-워터폴](../methodologies/하이퍼-워터폴.md)): *"기획은 같이, 실행은 AI 혼자, 리뷰는 다시 같이"* — 정확히 HITL 의 *Tiered* 적용.
- **CopilotKit · CrewAI · Anthropic Agent SDK** — 모두 HITL 인터럽트 표준 기능.

## 5. 강의 연결 포인트

- **"User → Orchestrator" 메시지** — 사람이 *모든 일을 직접 하는* 위치에서 *AI를 지휘하는* 위치로 이동. HITL 이 그 지휘의 매커니즘.
- **"좋은 결과는 우연이 아니라 설계"** — *어디에 사람을 끼워 넣을지 설계* 가 결과 신뢰도를 결정.
- **1층 하니스 도입 슬라이드** — 1층 하니스의 *권한 체크* 가 HITL 의 가장 작은 구현체.
- **`/harness` 5단계 흐름 슬라이드** — 5단계 중 *2번 단계가 HITL* (사용자와 논의).
- **이후 강의 워크플로우 (예고)** — *Dicom Viewer 만들기*에서 *기획·하니스 설계·리뷰* 3단계가 HITL, *실행* 1단계는 AI 자율.

## 한계와 주의

- **사용자 피로**: 너무 자주 묻는 HITL → 사용자가 *습관적 yes* 누름 → 실제 위험 못 인지. 검토 *밀도*가 핵심.
- **개입의 의미**: 사람이 *무엇을 검토하는지* 명확해야 함. *"raw JSON 100줄"* 던지지 말고 *요약*·*핵심 변경*만.
- **응답 지연**: Approve Before 는 사람이 *답할 때까지* 멈춤. 야간·주말·휴가 시 워크플로우 정체.
- **Trust calibration**: AI 가 *충분히 신뢰*받게 되면 HITL 빈도 자동 감소. → `auto` 모드 분류기가 푸는 문제.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code 퍼미션 모드](../tools/Claude-Code-퍼미션모드.md) — HITL 강도의 손잡이
- [Claude Code 1층 하니스](../tools/Claude-Code-1층-하니스.md) — *권한 체크* 가 HITL 매커니즘
- [Permissions & Hooks](../techniques/harness/permissions-and-hooks.md) — HITL 의 *결정론적 가드*
- [하이퍼-워터폴](../methodologies/하이퍼-워터폴.md) — HITL 의 *방법론적 적용*
- [Sycophancy](../phenomena/Sycophancy.md) — HITL 의 *사람*도 AI에 동조 위험. 검토 의식 필요
- [Orchestration](../techniques/Orchestration.md) — Multi-agent 환경에서의 HITL 통합

## 출처

- [LangChain — Human-in-the-loop (LangGraph Docs)](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) — `interrupt()` 표준
- [IBM — What Is Human In The Loop (HITL)?](https://www.ibm.com/think/topics/human-in-the-loop) — 정의 종합
- [Permit.io — Human-in-the-Loop for AI Agents (2026)](https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo) — 디자인 패턴
- [Waxell — HITL vs HOTL for AI Agents](https://www.waxell.ai/blog/human-in-the-loop-vs-human-on-the-loop-ai-agents) — 두 패턴 비교
- [tutorialQ — Human-in-the-Loop Orchestration](https://tutorialq.com/ai/multi-agent/human-in-the-loop) — 멀티에이전트와 결합
- [LiveKit — HITL Pattern for Voice Agents](https://livekit.com/blog/human-in-the-loop-voice-agents) — 음성 에이전트 적용
