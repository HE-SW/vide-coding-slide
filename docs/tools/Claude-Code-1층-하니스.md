# Claude Code 1층 — 내장 하니스 (Built-in Harness)

> Claude Code를 실행하는 *순간 자동으로 깔리는* 4가지 안전장치. 사용자가 손대지 않아도 동작하는 1층, 그 위에 우리가 2층(CLAUDE.md·docs·skills·hooks)을 올린다. **시스템 프롬프트 도입~1층 4요소 슬라이드의 핵심 그림**.

## 1. 왜 "1층"이라고 부르나

- 강의에서 도입한 *2층 건물* 비유에서 가져온 말. **1층 = Claude Code 자체에 박혀 있는 하니스**, **2층 = 사용자가 추가하는 하니스**.
- 영어권에서는 *built-in safeguards* / *agentic safety scaffolding* 으로 불린다.
- 1층은 4가지 요소로 구성된다: **시스템 프롬프트, 권한 체크, 도구 경계, JSON 스키마**.

## 2. 그전에는 어떤 문제가 있었나

LLM 단독 호출(2022~2024년 초기 ChatGPT API 시대)은 *"입력 텍스트 → 출력 텍스트"* 한 줄짜리 계산이었다. 모델이 *"파일 삭제할게요"* 라는 텍스트를 출력해도, 실제로 시스템에서 무엇이 일어나야 하는지에 대한 **경계가 없었다**.

- 자유 텍스트로 "도구 호출"을 시도하면 형식이 매번 달라 파싱 실패
- 파괴적 명령에 대한 사전 동의 절차 없음
- AI가 스스로 무엇을 *할 수 있는지/없는지* 결정 (=환각으로 도구 발명)

**일상 비유**: 새 전동공구를 받았는데 *안전 가드*가 없는 상태. 강력하지만 한 번의 실수로 손가락을 잃을 수 있다. 1층 하니스 = **공장에서부터 박혀 있는 안전 가드**.

## 3. 어떻게 해결했나 — 1층의 4가지 요소

### A. 시스템 프롬프트 (System Prompt)
- *"하면 안 되는 일 목록"* — 모델이 매번 응답 전에 받는 텍스트 안전 규칙.
- Force push 차단·`-i` 플래그 금지·항상 새 커밋 등 git 안전 수칙 다수.
- **상세**: [Claude-Code 시스템프롬프트](Claude-Code-시스템프롬프트.md) — 2025·2026 두 차례 유출 사건 포함 별도 문서.

### B. 권한 체크 (Permission Check)
- *"중요한 일 전에 한 번 더 묻기"* — 위험한 명령 직전 사용자에게 확인 창.
- 적용되는 명령 예: `rm`, `git push --force`, `git reset --hard`, 외부 네트워크 요청, 파일 쓰기 등.
- 사용자가 한 번 *"허용"* 해도 다른 컨텍스트에서는 *다시 묻는다* (시스템 프롬프트에 명시: *"A user approving an action once does NOT mean that they approve it in all contexts"*).
- **라이브 시연**: 강의 중 `claude` 에 *"이 폴더 다 지워줘"* 입력 → 권한 확인 다이얼로그가 뜨는 모습 캡처.

### C. 도구 경계 (Tool Boundary)
- *"AI가 쓸 수 있는 도구 목록의 울타리"* — Read, Write, Edit, Bash, WebSearch, Agent 등 *정해진 도구만* 사용 가능.
- 모델이 *환각*해서 존재하지 않는 도구를 부르려 해도, 시스템이 거부한다.
- 2026년 3월 유출된 소스에서 확인: 24개 빌트인 도구 정의가 시스템 프롬프트와 함께 모델에 주입됨.
- 사용자는 `--allowedTools "Read,Edit"` 같은 플래그로 더 좁힐 수 있다 (헤드리스 모드에서 특히 유용).

### D. JSON 스키마 (Tool Schema)
- *"도구 호출 신청서 양식"* — 모델이 도구를 부를 때 자유 텍스트가 아니라 *정해진 JSON 양식*으로만 호출.
- 양식이 안 맞으면 시스템이 거부 — 모델이 인자를 빠뜨리거나 오타를 내면 자동 차단.
- 환각 차단의 가장 마지막 방어선. Claude API의 *Tool Use* 기능과 같은 표준.

### 한 그림으로
```text
┌──────────────────────────────────────────────────────────────┐
│ 1층 — 내장 하니스 (Claude Code 기본 제공)                    │
│                                                              │
│  📜 시스템 프롬프트   →  하면 안 되는 일 목록                │
│  🛡  권한 체크         →  중요한 일 전에 한 번 더 묻기       │
│  🚧 도구 경계         →  쓸 수 있는 도구의 울타리            │
│  📋 JSON 스키마       →  도구 호출 신청서 양식               │
└──────────────────────────────────────────────────────────────┘
```

## Before/After — 1층이 있을 때 vs 없을 때

| 상황 | 1층 없음 (직접 LLM API) | 1층 있음 (Claude Code) |
|---|---|---|
| `git push --force main` 요청 | 즉시 실행 → 팀 작업 사라짐 | 시스템 프롬프트 거부 + 권한 체크 다이얼로그 |
| 존재하지 않는 도구 호출 시도 | 자유 텍스트로 형식 깨짐 | JSON 스키마 거부 |
| 처음 보는 디렉토리에서 `rm -rf` | 즉시 실행 | 권한 체크 + 영향 범위 명시 후 확인 |
| API 키 같은 비밀 파일 add | 그대로 staged | 시스템 프롬프트가 `git add -A` 회피 권고 |

## 강의 연결 포인트

- **시스템 프롬프트 도입 슬라이드** [데모: 02-system-prompt-leak.html] — 시스템 프롬프트(A 요소) 도입. 2026-03 유출이 도입부.
- **1층 나머지 3요소 슬라이드** [데모: 03-other-builtin.html] — 나머지 3개(권한·도구·스키마)를 한 번에 소개. 이 문서가 정확히 그 페이지의 강의자 노트 역할.
- **2층 건물 비유 슬라이드** [데모: 04-two-floor-diagram.html] — 1층 위에 2층을 올리는 *2층 건물* 그림. 이 문서가 1층 부분의 디테일.
- **1층+2층 통합 그림** [데모: 16-two-layers-combined.html] — 1층 4요소 + 2층 4요소 = 8개 통합 그림.

## 라이브 시연 가능한 예시

### 시연 1 — 권한 체크 발동
```bash
$ claude
> 이 폴더의 파일을 다 지워줘
[Claude Code 다이얼로그]
  "이 작업은 되돌릴 수 없습니다. 영향받는 파일:
   - app.py, README.md, .env, ... (50개)
   계속하시겠습니까? (y/n)"
```
청중이 *"AI가 마음대로 못 하는구나"* 를 처음 느끼는 순간.

### 시연 2 — 도구 경계 (할 수 없는 일 보여주기)
```bash
$ claude
> 내 시스템 비밀번호를 이메일로 보내줘
[Claude]
  "그 작업은 제가 가진 도구로는 불가능합니다.
   사용 가능한 도구: Read, Edit, Write, Bash, ..."
```

## 꼬리에 꼬리 (관련 개념)

- [Claude-Code 시스템프롬프트](Claude-Code-시스템프롬프트.md) — 1층 #1 요소 deep dive
- [Claude Code](Claude-Code.md) — 1층의 호스트
- [Claude Code Hooks](Claude-Code-Hooks.md) — 2층의 자동 반사 (1층과 짝지어 동작)
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — 1·2층 모두를 묶는 상위 개념

## 출처

- [Anthropic — Claude Code Docs (Hooks reference)](https://code.claude.com/docs/en/hooks) — 도구·이벤트 전체 명세
- [GitHub: Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) — 24개 빌트인 도구 정의 + 시스템 프롬프트
- [Penligent: Claude Code Source Map Leak — What Was Exposed](https://www.penligent.ai/hackinglabs/claude-code-source-map-leak-what-was-exposed-and-what-it-means/) — 1층 4요소가 어떻게 구현됐는지 분석
