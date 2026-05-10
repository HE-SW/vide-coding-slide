# Tool Use (도구 사용 / 함수 호출)

> LLM이 *텍스트만 뱉는* 게 아니라, **외부 함수·도구를 호출하고 결과를 받아 다시 사고하는** 능력. ChatGPT의 *function calling*, Claude의 *tool use* 가 같은 개념. 강의 전반에서 *"AI가 파일을 직접 읽고·고치고·실행"* 한다고 한 일이 모두 이 매커니즘 위에서 일어난다.

## 1. 왜 "Tool Use"라고 부르나

- 영어 *Tool*(도구) + *Use*(사용). 단순한 표현이지만 — *모델이 도구를 들고 일한다*는 발상의 전환을 담은 이름.
- **OpenAI**: 2023년 6월 *"function calling"* 으로 첫 도입. 그 후 *tool use* 로 명칭 정리.
- **Anthropic**: 2024년 5월 Claude 3 라인업에 *"Tool Use"* 정식 도입. *function calling* 보다 *tool use* 라는 더 일반화된 표현 선호.
- **Google Gemini / Meta Llama**: 2024~2025년 사이 모두 *function calling* / *tool use* 표준 채택.
- **2026 시점**: 모든 주요 LLM API가 표준 형식으로 tool use를 지원. *agent* 라는 단어가 의미 있는 *전제*.

## 2. 그전에는 어떤 문제가 있었나

LLM이 똑똑해도 — *바깥 세상*과 단절돼 있었다.

- *"오늘 날씨 알려줘"* → 모델은 날씨를 *모름*. 환각으로 답하거나 거절
- *"이 코드 실행해서 결과 알려줘"* → 모델은 *실행 환경*이 없음
- *"GitHub 이슈에 코멘트 달아줘"* → 모델은 *행동*할 수 없음. 텍스트만 뱉음

→ LLM이 *텍스트 생성기*에서 *행동하는 에이전트*로 진화하려면 **외부 호출**이 필요했다.

**일상 비유**: 천재 학생이 *책상 앞에 묶여* 있다. 모르는 게 있어도 도서관·인터넷·계산기를 못 쓴다. *외부 도구를 들 수 있게* 해주는 게 tool use.

## 3. 어떻게 해결했나 — 구조화된 함수 호출

### (1) 흐름

```text
1. 사용자: "오늘 서울 날씨 알려줘"

2. API 요청 시 모델에게 *사용 가능한 도구 목록*을 함께 전달:
   tools = [{
     name: "get_weather",
     description: "도시의 현재 날씨를 가져온다",
     input_schema: { city: string }
   }]

3. 모델 응답:
   {
     "type": "tool_use",
     "tool_name": "get_weather",
     "tool_input": { "city": "Seoul" }
   }

4. 클라이언트 코드가 실제로 get_weather("Seoul") 호출 → "맑음, 22도"

5. 결과를 모델에게 다시 전달

6. 모델 최종 응답: "오늘 서울은 맑고 22도입니다."
```

→ 모델은 *직접 호출*하지 않는다. *호출하고 싶은 의도*를 JSON으로 표현하고, *클라이언트가 실행 후 결과를 다시 모델에게 입력*. 이게 [Claude Code 1층 하니스](../tools/Claude-Code-1층-하니스.md)의 *JSON 스키마*가 작동하는 매커니즘.

### (2) 2026 시점의 핵심 기능

**Parallel Tool Use** — 여러 도구를 *동시에* 호출. 예: GitHub 이슈 + Slack 메시지 + DB 조회를 *순차*가 아닌 *병렬*로. Claude 4 라인업은 기본 활성화.

**Programmatic Tool Calling** (2026 신규) — Claude가 도구 결과를 *코드*로 처리한 뒤 *최종 결과만* 다음 모델 호출에 전달. 토큰 절약 + 더 복잡한 도구 오케스트레이션.

**Tool Search Tool** (2026 신규) — 모델이 *어떤 도구가 있는지* 동적으로 검색. 도구가 수백 개일 때 컨텍스트 절약.

**Tool Use Examples** (2026 신규) — 도구 정의에 *예시 호출*을 함께 제공해 모델 정확도 ↑.

## Before / After

```text
[BEFORE — 도구 없는 LLM (2022)]
USER: "이 함수 짜고 테스트해줘"
AI:   "def fib(n): ..."  (텍스트 출력만)
USER: (직접 코드 복사 → 실행 → 에러 보고 → 모델에게 다시 설명)
   ...반복

[AFTER — Tool Use (Claude Code, 2026)]
USER: "이 함수 짜고 테스트해줘"
AI:   1. Write 도구로 fib.py 생성
      2. Bash 도구로 pytest 실행
      3. 1개 테스트 실패 결과 받음
      4. Edit 도구로 수정
      5. Bash 도구로 재실행 → 모두 통과
      "완료. fib(10) = 55, 모든 테스트 통과"
```

같은 모델이 — **외부 호출 능력 유무**로 *완전히 다른 도구*가 된다.

## 라이브 시연 가능한 예시

```bash
[강의 화면 — Claude Code 안]
> "현재 이 디렉토리에서 파이썬 파일이 몇 개야?"

[Claude Code 출력]
🔧 Bash 도구 호출: find . -name '*.py' | wc -l
   결과: 23
"이 디렉토리에 파이썬 파일은 23개 있습니다."
```

🔧 아이콘이 뜨는 *바로 그 순간*이 청중에게 *"이게 tool use가 일어나는 모습"*. 텍스트가 도구 호출로 *체화*되는 시점.

## Tool Use 와 다른 개념의 관계

| 개념 | tool use 와의 관계 |
|---|---|
| **MCP** | tool use를 *표준화된 외부 도구*로 확장한 프로토콜. tool use가 *기반*, MCP가 *생태계*. |
| **Function Calling** | OpenAI에서 부르는 같은 개념의 다른 이름. |
| **Agent** | tool use 를 *반복적*으로 활용해 *목표 달성*까지 도달하는 시스템 = Agent. tool use 없는 agent는 불가능. |
| **JSON Schema** | tool 의 *호출 양식*. 양식 안 맞으면 시스템이 거부 — 환각의 마지막 방어선. |

## 강의 연결 포인트

- 직접 슬라이드는 없음. 그러나 *"AI가 파일을 직접 읽고·고치고·실행"* 한다는 강의 메시지의 *기술적 토대*.
- **1층 하니스 4요소 슬라이드** [데모: 03-other-builtin.html] — *JSON 스키마* 가 1층 하니스의 한 요소로 등장. 이 문서가 그 매커니즘의 더 깊은 설명.
- **하니스 세팅 전반** — Claude Code의 모든 행동(Read, Write, Edit, Bash, ...)이 결국 tool use 호출. **tool use 가 없으면 Claude Code 자체가 불가능**.

## 꼬리에 꼬리 (관련 개념)

- [LLM](LLM.md) — tool use 의 주체
- [Claude Code 1층 하니스](../tools/Claude-Code-1층-하니스.md) — *도구 경계*·*JSON 스키마* 두 요소가 tool use 의 안전장치
- [MCP](../tools/MCP.md) — tool use 를 외부 시스템과 *표준 프로토콜*로 연결
- [서브에이전트](../tools/서브에이전트.md) — tool use를 가진 작은 Claude 인스턴스들의 분업
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — tool use 를 묶는 상위 개념
- [환각](../phenomena/환각.md) — JSON 스키마는 *환각으로 도구 발명*을 막는 방어선

## 출처

- [Anthropic — Tool use with Claude (Claude API Docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — 공식 명세
- [Anthropic — How to implement tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use) — 구현 가이드
- [Anthropic — Programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) — 2026 신규
- [Anthropic — Introducing advanced tool use on the Claude Developer (Engineering Blog)](https://www.anthropic.com/engineering/advanced-tool-use) — Tool Search Tool · Programmatic Tool Calling · Tool Use Examples 3종
- [inkeybit: Claude Tool Use & Function Calling — Complete Developer Guide (2026)](https://www.inkeybit.com/blog/claude-tool-use-function-calling) — 입문~심화
- [ofox.ai: Function Calling & Tool Use — GPT, Claude, Gemini (2026)](https://ofox.ai/blog/function-calling-tool-use-complete-guide-2026/) — 모델 간 비교
