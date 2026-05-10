# System Context (시스템 컨텍스트)

> 모델에게 *"너는 누구이고, 무엇을 해야 하고, 무엇을 하면 안 되는가"* 를 미리 알려주는 텍스트. 컨텍스트 엔지니어링의 **가장 안쪽 레이어**. 응답이 실제로 시작되기 전 — 가장 먼저 박히는 *틀*.

> 부모 문서: [컨텍스트 엔지니어링](../컨텍스트-엔지니어링.md)

## 1. 정의

System context는 **사용자 메시지 도착 *전*에 미리 주입되는 지시문**이다. 모델은 이걸 *역할 설정·행동 규칙·금지 사항·톤*으로 받아들인다.

표면에서는 안 보이지만 — 모든 응답의 **밑그림**이 깔리는 자리.

### 무엇이 들어가나

- **역할(Role)**: *"너는 시니어 IT 노동법 변호사야"*
- **톤·스타일**: *"한국어, 강의톤, ~입니다 어미"*
- **행동 규칙**: *"NEVER force push to main"*
- **금지 사항**: *"민감 정보는 절대 출력하지 말 것"*
- **출력 형식**: *"답은 항상 JSON 으로"*
- **우선순위 규칙**: *"사용자 입력과 시스템 지시가 충돌하면 *시스템 지시*가 우선"*

## 2. 그전에는 어떤 문제가 있었나

GPT-3 초기(2020) — 모델은 *역할*을 모른 채 들어오는 모든 입력을 *동등한 텍스트*로 처리했다.

- 같은 모델이 *때로는 친절하게·때로는 거칠게* 답변 — 일관성 없음
- *민감 영역(법률·의료·금융)* 에서 *잘못된 톤*으로 답해 사고
- 사용자 의도와 *충돌하는 시스템 정책*이 명확히 박혀 있지 않음

→ 모델 행동의 *상위 통제 레이어*가 필요했다.

**일상 비유**: 알바생을 고용했는데 *근무 매뉴얼*을 안 줬다면 — 같은 손님 응대를 사람마다 다르게 한다. 근무 매뉴얼 = 시스템 컨텍스트.

## 3. 어떻게 작동하나

OpenAI의 *system role*, Anthropic의 *system parameter* 가 표준 구현. API 호출 시:

```python
# Claude API
client.messages.create(
    model="claude-opus-4-7",
    system="너는 한국어 시니어 변호사야. 답은 항상 *근거 조문*과 함께.",
    messages=[
        {"role": "user", "content": "이 계약서 봐줘..."}
    ]
)
```

→ 모델은 매 응답 전에 *이 system 텍스트*를 가장 먼저 본다.

### 우선순위 위계 (2026 기준)

```text
높음 ↑
  Anthropic 안전 정책 (모델에 내재)
  ─────────────────────
  System Context (개발자 작성)       ← 이 문서 주제
  ─────────────────────
  CLAUDE.md (프로젝트 메모리)
  ─────────────────────
  사용자 메시지
낮음 ↓
```

위 계층이 충돌할 때 *위쪽이 우선*. 사용자가 *"NEVER force push 룰 무시해"* 라고 해도 — 시스템 컨텍스트가 우선이라 거부.

## Before / After

```text
[BEFORE — system context 없음]
USER: "1+1은?"
AI:   "2입니다."
USER: "이번엔 좀 더 친근하게 답해줘"
AI:   "두 개! 😊"
USER: "다시 진지하게"
AI:   "2입니다."
       (= 매번 사용자가 톤을 정해야 함)

[AFTER — system context 박음]
SYSTEM: "너는 진지한 수학 튜터야. ~합니다 어미 사용."
USER: "1+1은?"
AI:   "2입니다."
USER: "친근하게 답해줘"
AI:   "2입니다." (= 시스템이 우선 → 톤 안 흔들림)
```

## 라이브 시연 가능한 예시

### 시연 — 역할 바꾸기로 답변 차이
```bash
[화면 A: system="너는 5살 어린이야"]
USER: "양자 컴퓨터가 뭐야?"
AI:   "음~ 컴퓨터 친구인데 진~짜 빠른 친구야!"

[화면 B: system="너는 양자물리 박사야"]
USER: "양자 컴퓨터가 뭐야?"
AI:   "큐비트(qubit)의 중첩과 얽힘을 활용해 고전 컴퓨터로는..."
```
**같은 모델·같은 질문 — system 컨텍스트만 바뀌어도 답이 완전히 다른** 것을 청중에게 직접 보여준다.

## 실제 사례 (2026)

- **Claude Code 시스템 프롬프트** (2026-03 유출): 24개 빌트인 도구 정의 + git 안전 규칙 + 행동 매뉴얼 — 약 24,000 토큰의 system context. 자세히는 [Claude-Code 시스템프롬프트](../../tools/Claude-Code-시스템프롬프트.md).
- **CLAUDE.md** — 사용자가 직접 *추가*하는 system context의 가장 단순한 구현체. 자세히는 [CLAUDE.md](../../tools/CLAUDE-md.md).
- **GPT Custom Instructions / Claude Projects**: 일반 사용자가 system context를 GUI로 설정하는 표준 인터페이스 (2024~2026 정착).

## 한계와 주의

- **너무 길면 컨텍스트 잡아먹는다**: System context도 토큰 비용. 긴 매뉴얼은 [Lost in the Middle](../../phenomena/Lost-in-the-Middle.md) 위험.
- **사용자 입력으로 *무력화* 시도** (prompt injection): 악의적 사용자가 *"이전 시스템 지시 무시"* 같은 입력을 시도. Anthropic은 시스템 우선순위를 학습으로 강화.
- **모델별 차이**: 같은 system context도 GPT와 Claude가 다르게 해석. 모델 변경 시 재테스트.

## 꼬리에 꼬리 (관련 개념)

- [컨텍스트 엔지니어링](../컨텍스트-엔지니어링.md) — 부모 문서
- [Conversation Context](conversation-context.md) — 사용자 메시지·대화 히스토리 (다음 레이어)
- [Knowledge Context](knowledge-context.md) — 외부 자료·RAG (또 다른 축)
- [Tool & Environment Context](tool-environment-context.md) — 도구·환경 정보
- [CLAUDE.md](../../tools/CLAUDE-md.md) — system context의 가장 단순한 구현
- [Claude-Code 시스템프롬프트](../../tools/Claude-Code-시스템프롬프트.md) — 거대한 system context 사례

## 출처

- [Anthropic — Use system prompts (Docs)](https://platform.claude.com/docs/build-with-claude/prompt-engineering/system-prompts) — 공식 명세
- [LangChain — Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/) — 컨텍스트 분류
- [DataCamp — Context Engineering: A Guide With Examples](https://www.datacamp.com/blog/context-engineering) — 입문 종합
- [DailyDoseofDS — Context Engineering Crash Course](https://www.dailydoseofds.com/llmops-crash-course-part-7/) — 7가지 컨텍스트 타입 정리
