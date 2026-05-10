# Claude Code 퍼미션 모드 (Permission Modes)

> Claude Code가 *얼마나 자율적으로* 일할지 결정하는 5+1가지 모드. **Shift+Tab 으로 사이클**. *"AI에게 어디까지 내맡길 것인가"* 라는 강의 핵심 질문의 *작동 손잡이*.

## 1. 왜 "퍼미션 모드"라고 부르나

- **Permission(허용) + Mode(모드)**. *"AI가 어떤 행동을 하기 전에 사용자에게 묻는 정도"* 를 단계로 나눈 것.
- Claude Code 는 *Auto Mode* (2025-말 출시), *Plan Mode*, *AcceptEdits*, *bypassPermissions* 등을 거치며 단계적으로 추가됨.
- **2026-05 시점 기준**: 5가지 표준 모드 + Team/Enterprise 전용 1가지 = **5+1**.

## 2. 그전에는 어떤 문제가 있었나

LLM 코딩 도구가 *모든 행동에 매번 사용자 확인*을 요청하면 — 너무 느리다. 반대로 *모든 행동을 자유 실행*하면 — 사고 위험.

- *5분짜리 자동화* 작업이 *200번의 확인 다이얼로그*에 막혀 1시간이 됨
- 그렇다고 확인을 다 빼면 → AI가 `rm -rf` 같은 명령을 무심코 실행
- *"안전과 속도 사이"* 의 양자택일

→ 작업의 *위험도*에 따라 *다르게 동작*하는 모드 시스템이 필요했다.

**일상 비유**: 자동차 운전 모드 — *Eco / Normal / Sport* 전환 손잡이. 같은 차가 *언제는 안전·언제는 빠르게*. Claude Code 의 5가지 모드도 같은 발상.

## 3. 다섯 가지 모드 — 한눈에

```text
   더 안전 ←──────────────────────────────────→ 더 자율
   ┌──────┐  ┌──────────┐  ┌────────┐  ┌──────┐  ┌──────────────────┐
   │ plan │  │ default  │  │ accept │  │ auto │  │ bypassPermissions │
   │      │  │ (matrix) │  │ Edits  │  │      │  │  (─dangerously─)   │
   └──────┘  └──────────┘  └────────┘  └──────┘  └──────────────────┘
```

| 모드 | 한 줄 요약 | 동작 |
|---|---|---|
| **plan** | *읽기만* — 계획만 짜고 실행 ❌ | Read·Grep만 가능. Edit·Bash 차단. 종료 시 ExitPlanMode로 계획 승인 받음 |
| **default** | 매 위험 행동마다 확인 | rm·force-push·외부 호출 등 매번 다이얼로그 |
| **acceptEdits** | 파일 편집 자동 승인, 시스템 명령은 확인 | Edit·Write·간단한 Bash(mkdir/touch/rm/cp/sed) 자동. 그 외는 확인 |
| **auto** ⚠ Team plan 전용 | *분류기*가 행동을 보고 결정 | Sonnet 4.6 이상 모델 + 백그라운드 분류기가 안전/위험 자동 판단 |
| **bypassPermissions** | 모든 확인 스킵 — *완전 자율* | `--dangerously-skip-permissions` 플래그. 파괴 위험 ↑↑↑ |

### 추가 — `dontAsk`

- 특정 도구·패턴에 한해 *항상 허용* 등록. *전체 모드 변경 없이* 미세 조정.
- 예: *내 워크트리에서는 git commit 은 매번 묻지 말 것*.

## 모드 전환 — 두 가지 방법

### (1) 세션 중 — Shift+Tab 사이클
```text
Shift+Tab 1회: default → acceptEdits
Shift+Tab 2회: acceptEdits → plan
Shift+Tab 3회: plan → default (사이클)
```
auto·bypassPermissions 는 사이클에 포함 안 됨 (의도적 — 실수로 진입 방지).

### (2) 영구 설정 — `settings.json`
```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```
세션마다 *내 선호 모드*로 자동 시작.

## Before / After

### 같은 작업, 다른 모드

```text
작업: "이 폴더 코드 리팩토링하고 테스트 통과시켜줘"

[default 모드]
- "Edit src/auth.py 해도 될까요? (y/n)"
- "Bash: pytest 실행해도 될까요? (y/n)"
- "Edit src/auth.py 다시 해도 될까요? (y/n)"
  ... 30번의 다이얼로그
- 사용자가 매번 확인 → 30분

[acceptEdits 모드]
- 코드 변경 자동
- 테스트 실행 자동
- 5분 후 "완료. 12개 테스트 통과"

[plan 모드]
- 실행 0건
- "리팩토링 계획서 작성: 1) auth.py 분리 2) ..."
- 사용자 승인 후 다른 모드로 전환해 실행

[auto 모드]
- 분류기가 *읽기·편집·테스트* 는 자동, *외부 호출·파일 삭제* 는 확인
- 균형 잡힌 자동화
```

## 라이브 시연 가능한 예시

### 시연 1 — Plan 모드 진입
```bash
[강의 중]
> Shift+Tab Shift+Tab  (default → acceptEdits → plan)
[Plan 모드로 전환됨]

> "이 코드베이스 보안 점검해줘"
→ Claude: 읽기·검색만 수행. 코드 변경 ❌
→ ExitPlanMode 호출 → 사용자 검토 → 승인 시 acceptEdits 등으로 전환해 실행
```

### 시연 2 — bypassPermissions 의 위험성
```bash
[설명용 — 실제 시연은 ⚠ 위험]
$ claude --dangerously-skip-permissions
> "이 폴더 정리해줘"
→ rm -rf 도 묻지 않고 실행 → 데이터 소실 가능

→ 절대 *프로덕션 환경*에서 쓰지 말 것. CI/특수 자동화 한정.
```

## 실제 사례 (2026 기준)

- **개인 개발자 표준**: `acceptEdits` 가 가장 흔한 디폴트. 편집 빠르고, 파괴 명령은 확인.
- **팀 개발**: `auto` 모드 (Team plan 필요). 분류기가 위험 자동 차단 + 빠른 작업 흐름.
- **CI/CD 파이프라인**: `bypassPermissions` + 컨테이너 격리. 어차피 컨테이너가 *깨져도 되니까* 안전.
- **시연·강의·중요 PR 리뷰**: `plan` 모드. 읽기만 해서 *분석·계획만* 받고, 사용자가 검토.

## 강의 연결 포인트

- 직접 슬라이드는 없음. 그러나 강의 *"AI를 어디까지 믿을 것인가"* 메시지의 *기술적 손잡이*.
- **1층 하니스 도입 슬라이드** [데모: 02-system-prompt-leak.html, 03-other-builtin.html] — *권한 체크* 가 1층 하니스의 한 요소로 등장. 퍼미션 모드는 그 *권한 체크의 강도*를 사용자가 조절하는 손잡이.
- **`/harness` 워크플로우 슬라이드** — 헤드리스 모드(`claude -p`)에서는 통상 `bypassPermissions` 또는 `auto` 모드를 사용. 사람의 입력 없이 흘러가는 매커니즘.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code 1층 하니스](Claude-Code-1층-하니스.md) — *권한 체크* 가 퍼미션 모드의 동작 무대
- [Claude Code Hooks](Claude-Code-Hooks.md) — `PreToolUse` hook 으로 *모드와 별개로* 추가 차단 가능
- [Claude Code 헤드리스 모드](Claude-Code-Headless-모드.md) — 자동화 시 어떤 모드를 쓸지 결정
- [Claude Code](Claude-Code.md) — 모드 호스트
- [Claude Code 입력 문법](Claude-Code-입력문법.md) — `Shift+Tab` 으로 모드를 *키 한 번에* 순환하는 단축
- [andrej-karpathy-skills](andrej-karpathy-skills.md) — *목표 기반 검증* 패턴은 `plan` 모드의 본질

## 출처

- [Anthropic — Choose a permission mode (Claude Code Docs)](https://code.claude.com/docs/en/permission-modes) — 공식 명세
- [Anthropic — Configure permissions (Agent SDK)](https://platform.claude.com/docs/en/agent-sdk/permissions) — SDK 사용 시 모드 지정
- [ClaudeFa.st: Claude Code Permissions Safe vs Fast](https://claudefa.st/blog/guide/development/permission-management) — 모드별 트레이드오프
- [SmartScope: Claude Code Auto Approve Guide (2026)](https://smartscope.blog/en/generative-ai/claude/claude-code-auto-permission-guide/) — `auto` 모드 deep dive
- [wmedia.es: Control How Much Autonomy with 6 Permission Modes](https://wmedia.es/en/tips/claude-code-permission-modes-shift-tab) — Shift+Tab 사이클 설명
- [Claude Lab: Permission Modes Deep Dive — Auto/Plan/Hooks (2026)](https://claudelab.net/en/articles/claude-code/claude-code-permission-modes-production-security-guide) — 프로덕션 보안 관점
- [Pasquale Pillitteri: dangerously-skip-permissions Guide (2026)](https://pasqualepillitteri.it/en/news/141/claude-code-dangerously-skip-permissions-guide-autonomous-mode) — bypass 모드 위험성 분석
