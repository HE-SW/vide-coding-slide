# Meta-Prompting · Prompt Chaining · ReAct

> *프롬프트가 프롬프트를 만든다*. 작업을 *여러 단계로 쪼개* 모델이 스스로 다음 프롬프트를 생성하거나, *추론과 행동을 번갈아* 수행하는 패턴. 단발 프롬프트의 한계를 *프롬프트 *흐름** 으로 푸는 방향.

> 부모 문서: [프롬프트 엔지니어링](../프롬프트-엔지니어링.md)

## 1. 정의 — 세 가지 묶음

### Meta-Prompting
*"프롬프트를 만드는 프롬프트"*. 모델에게 *어떤 프롬프트가 좋을지* 먼저 묻고, 그 답을 다시 모델에 입력.

```text
[1단계 — 메타]
"이 작업에 가장 효과적인 프롬프트를 작성해줘:
 작업 = '회사 휴가 정책 챗봇'"

→ AI: "다음 프롬프트를 추천합니다:
       '너는 친절한 HR 도우미야. 답할 때..."

[2단계 — 실행]
[1단계의 답을 새 프롬프트로]
"너는 친절한 HR 도우미야. 답할 때..."

→ AI: "휴가 정책에 대해 어떻게 도와드릴까요?"
```

### Prompt Chaining (프롬프트 체이닝)
*큰 작업을 작은 프롬프트의 *순차 호출*로 분해*. 각 호출의 *출력*이 다음 호출의 *입력*.

```text
[Chain]
1) "이 책의 목차 만들어줘 (10장)" → 목차 X
2) "X의 1장 초안 작성" → 초안 Y1
3) "Y1을 검토해 누락 부분 추가" → 보완 Y1'
4) "X의 2장 초안 작성, Y1'와 일관성 유지" → ...
```

### ReAct (Reason + Act, 2022)
*추론*과 *행동*을 *번갈아* 한 응답 안에 섞는 패턴. Tool use 시대의 표준.

```text
[ReAct 1턴]
사고: "사용자가 *오늘 서울 날씨*를 물었다. 검색이 필요하다."
행동: get_weather("Seoul") 호출
관찰: "맑음, 22도"
사고: "이 정보로 답할 수 있다."
응답: "오늘 서울은 맑고 22도입니다."
```

## 2. 그전에는 어떤 문제가 있었나

단일 프롬프트로는 *큰 작업*을 못 다룬다.

- 책 한 권 쓰기 → 한 프롬프트에 다 넣기 불가능 (컨텍스트 한계)
- 복잡한 분석 → 한 번에 하기엔 *추론 길이* 한계
- *사용자가 어떤 프롬프트를 써야 할지* 모름 → 비전문가에게 진입 장벽

→ *프롬프트가 흐르는 시스템*이 필요했다.

**일상 비유**: 책 쓰기를 *한 단락에* 다 하려는 작가는 없다. *목차 → 각 장 초안 → 검토 → 수정* 의 단계로 흐른다. Prompt chaining 이 그 *단계 분리*를 LLM에 가져온다.

## 3. 셋의 관계

```text
Meta-Prompting       "어떤 프롬프트가 좋은가" 를 모델이 결정
                       ↓
Prompt Chaining      여러 프롬프트를 *순차*로 흘림
                       ↓
ReAct                각 프롬프트 안에서 *추론 + 도구 호출 + 관찰*
                     이 한 응답 안에 *interleaved*
```

→ 셋은 *상보적*. 같이 쓸 수 있고, 실제로 자주 결합.

## Before / After

### 글쓰기 작업

```text
[BEFORE — 단일 프롬프트]
"바이브코딩 강의 전체 분량의 모든 슬라이드 만들어줘"
→ AI: 한 번에 토큰 폭발 / 일관성 무너짐 / 앞뒤 회차가 서로 연결 안 됨

[AFTER — Prompt Chaining]
1) "강의 전체 목차 짜줘"  → 80개 섹션 목록
2) "첫 회차 19개 섹션 각각의 1줄 요약" → 회차 outline
3) "첫 회차 §1 본문 작성, 비개발자 톤" → §1
4) "§1 와 일관성 있게 §2 작성" → §2
   ...반복
```

### 코드 작업

```text
[BEFORE]
"이 레포 보안 점검하고 다 고쳐줘"  (= 답이 흐릿)

[AFTER — ReAct + Chaining]
1) ReAct: 코드 그렙 → 의심 패턴 발견 → 분석
2) ReAct: 추가 도구 호출 → 컨텍스트 확보
3) ReAct: 수정 코드 작성 → 테스트 실행 → 통과 확인
4) 다음 의심 패턴으로 → 반복
```

## 라이브 시연 가능한 예시

### 시연 — Prompt Chaining 가시화
```bash
[화면 — Claude Code]
> "/harness"

[Claude의 chained prompts (시각화)]
Phase 1 prompt: "PRD를 읽고 구현 계획 수립"
  → 출력: 5개 phase 계획

Phase 2 prompt: "Phase 1의 계획을 바탕으로 Phase 1 코드 작성"
  → 출력: 코드 + 테스트

Phase 3 prompt: "Phase 2의 결과 + 새 요구사항으로 Phase 3 시작"
  ...
```

청중에게: *"`/harness` 한 줄이 — 사실은 *5개의 chained prompt*가 자동으로 흐르는 것."*

## 4. ReAct 더 자세히

ReAct (Yao et al., 2022, *"ReAct: Synergizing Reasoning and Acting"*) 가 도입한 핵심:

```text
T1  Thought: "사용자가 X를 물음. Y가 필요하다"
T1  Action: search("X 관련 자료")
T1  Observation: "결과 = ..."

T2  Thought: "결과로 답이 부족. Z도 필요"
T2  Action: search("Z")
T2  Observation: "..."

T3  Thought: "이제 답할 수 있다."
T3  Final Answer: "..."
```

→ 모든 *agentic* 도구의 표준 매커니즘. Claude Code·Cursor·ChatGPT 모두 ReAct 구조 사용.

## 한계

- **Chain 의 길이**: 길어지면 *오류 누적*. Phase 5에서 Phase 1의 결정이 *왜곡*돼 흐를 위험.
- **비용**: 각 단계마다 별도 API 호출. 비용 ↑.
- **상태 관리**: chain 사이에 *어떤 정보를 전달*할지 설계가 핵심. 이게 [Conversation Context](../context/conversation-context.md) · [문서 주도 개발](../문서-주도-개발.md) 이 풀려는 문제.
- **사람의 개입 시점**: 완전 자동 chain 은 위험. *중요 단계마다* 사람 검토 (예: [하이퍼-워터폴](../../methodologies/하이퍼-워터폴.md) 의 5단계).

## 꼬리에 꼬리 (관련 개념)

- [프롬프트 엔지니어링](../프롬프트-엔지니어링.md) — 부모 문서
- [Chain-of-Thought](chain-of-thought.md) — Meta-prompting 으로 *적절한 CoT* 생성 가능
- [Self-Consistency](self-consistency.md) — Chain 의 각 단계에 적용 가능
- [Tool Use](../../concepts/Tool-Use.md) — ReAct 의 *Action* 부분의 매커니즘
- [하니스 엔지니어링](../하니스-엔지니어링.md) — Prompt chaining 을 *프로젝트 워크플로우*로 굳힌 것
- [Claude Code Headless 모드](../../tools/Claude-Code-Headless-모드.md) — Chain 호출의 표준 매커니즘

## 출처

- [ReAct: Synergizing Reasoning and Acting (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — 원논문
- [Meta-Prompting (Suzgun et al., 2024)](https://arxiv.org/abs/2401.12954) — Meta-prompting 형식 정리
- [Prompt Chaining — Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/skills/prompt_chaining) — 실무 패턴
- [Prompting Guide — ReAct](https://www.promptingguide.ai/techniques/react) — 입문
