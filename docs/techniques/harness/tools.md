# Tools (도구) — 하니스의 *손*

> AI가 *말만 하는 게 아니라 행동하게 만드는 부품*. 파일 읽기·코드 실행·웹 검색·API 호출 같은 *능력의 묶음*. 하니스 엔지니어링에서 *모델이 세계와 닿는 인터페이스*.

> 부모 문서: [하니스 엔지니어링](../하니스-엔지니어링.md)

## 1. 정의

Tools 는 모델에게 부여되는 **함수 호출 가능한 능력의 집합**. 각 tool은:
- *이름·설명·입력 스키마* 가 정의됨
- 모델이 *호출 의도*를 JSON으로 표현
- 클라이언트가 실제로 실행 후 결과를 *모델에 다시 입력*

자세한 매커니즘은 [Tool Use](../../concepts/Tool-Use.md).

## 2. 그전에는 어떤 문제가 있었나

LLM이 *텍스트 생성기*에서 멈추면 — *행동의 결과를 보고 다음을 결정*할 수 없다.

- "이 코드 짜줘" → 텍스트만 출력. *실행해서 검증*은 사람 몫
- "이 PR 리뷰해줘" → 의견만 텍스트. *실제 GitHub에 코멘트 작성*은 불가
- "테스트 통과시켜줘" → 코드 수정안만 출력. *반복 실행·재시도*는 사람이 매번 입력

→ 모델에게 *실행 능력*을 주는 표준이 필요했다.

## 3. Claude Code 의 Tools (24개, 2026-03 유출 기준)

### Filesystem (파일 시스템)
- `Read` — 파일 내용 읽기
- `Edit` — 파일 *부분* 수정
- `Write` — 파일 *전체* 쓰기 (덮어쓰기)

### Shell
- `Bash` — 셸 명령 실행 (`ls`, `pytest`, `git` 등)

### Search
- `Grep` — 정규식·키워드 검색
- `WebSearch` — 웹 검색
- `WebFetch` — URL 내용 가져오기

### Agent
- `Agent` — 서브에이전트 호출

### Notebook
- `NotebookEdit` — Jupyter 노트북 편집

### Task Management
- `TaskCreate`, `TaskUpdate`, `TaskList` ... — 작업 관리

### MCP — 외부 도구 통합
- `mcp__server-name__tool-name` — 모든 MCP 서버 도구가 이 형식으로 노출 (자세히는 [MCP](../../tools/MCP.md))

## 도구 설계 원칙 (Anthropic 권고)

### (1) *최소 권한* (Principle of Least Privilege)
이 작업에 *꼭 필요한* 도구만 부여. 코드 리뷰 서브에이전트에게 `Bash`·`Write`는 줄 필요 없음.

```text
[잘못된 설계]
agent: code-reviewer
tools: [Read, Edit, Write, Bash, WebSearch]   ← 너무 많음

[올바른 설계]
agent: code-reviewer
tools: [Read, Grep]   ← 읽기만
```

### (2) *명확한 description*
도구 이름·설명이 모호하면 모델이 *언제 호출할지* 잘못 판단. 좋은 설명은:
- *언제 쓰나* 명시
- *어떤 입력*을 받는지
- *어떤 결과*가 나오는지

### (3) *오류 메시지의 품질*
도구 호출 실패 시 stderr 가 *모델에 다시 입력*된다. 좋은 오류는:
- *왜 실패했는지* 명시
- *수정 방향* 힌트

```text
[나쁜 오류]
"Error: 5"

[좋은 오류]
"FileNotFoundError: 'config.yaml' not found in current directory.
 Try: 1) check working dir with Bash 'pwd'
      2) create the file with Write
      3) use a different filename"
```

## Before / After

```text
[BEFORE — Tools 없는 LLM]
USER: "이 함수 짜고 테스트도 통과시켜줘"
AI:   "def fib(n): ..."  (텍스트만)
USER: (사람이 직접 코드 복붙 → 실행 → 에러 → 다시 보고)

[AFTER — Tools 있는 Claude Code]
USER: "이 함수 짜고 테스트도 통과시켜줘"
AI:   🔧 Write fib.py
      🔧 Write test_fib.py
      🔧 Bash: pytest → 1 fail
      🔧 Edit fib.py
      🔧 Bash: pytest → all pass
      "완료. fib(10) = 55"
```

## 라이브 시연 가능한 예시

```bash
[강의 화면]
> "이 디렉토리에서 *.md 파일이 몇 개야?"

[Claude Code 출력]
🔧 Bash: find . -name "*.md" | wc -l
   결과: 47

"47개입니다."
```

🔧 아이콘이 뜨는 *바로 그 순간* = 도구가 작동하는 가시화. 청중에게 *"AI가 *행동*했다"* 를 직관적으로 전달.

## 4. 실제 사례

- **Claude Code 24개 빌트인 + MCP 무한 확장** (2026): 가장 풍부한 도구 생태계
- **Cursor / Windsurf**: 비슷한 도구 셋. *Apply* / *Run Command* 등
- **OpenAI Code Interpreter / Computer Use**: GUI 자동화까지 포함한 도구
- **GitHub Copilot Workspace**: 프로젝트 단위 도구 통합

## 한계와 주의

- **도구가 많을수록 *어떤 도구를 부를지* 결정의 부담**: 100개 넘으면 정확도 ↓. → MCP의 *Tool Search Tool* 이 푸는 문제 (자세히는 [MCP](../../tools/MCP.md)).
- **도구 결과의 *컨텍스트 폭증***: 10MB 로그가 컨텍스트로 들어오면 [Lost in the Middle](../../phenomena/Lost-in-the-Middle.md). 요약·필터링 필수.
- **권한 최소화 vs 기능**: 도구를 너무 좁히면 *해야 할 일을 못 함*. 균형이 핵심.

## 꼬리에 꼬리 (관련 개념)

- [하니스 엔지니어링](../하니스-엔지니어링.md) — 부모 문서
- [Tool Use](../../concepts/Tool-Use.md) — Tools 의 *기술적 매커니즘*
- [MCP](../../tools/MCP.md) — Tools 의 외부 확장 표준
- [서브에이전트와 분업](subagents-and-delegation.md) — Tools 를 위임받는 일꾼들
- [퍼미션·훅](permissions-and-hooks.md) — Tools 호출 *직전*에 끼어드는 안전장치
- [Claude Code 1층 하니스](../../tools/Claude-Code-1층-하니스.md) — *도구 경계*가 1층의 한 요소

## 출처

- [Anthropic — Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — 공식 명세
- [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — 도구 설계 원칙
- [Awesome Harness Engineering](https://github.com/ai-boost/awesome-harness-engineering) — 도구·패턴·관측성
