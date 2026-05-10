# Subagents & Delegation (서브에이전트와 분업)

> *큰 일을 작은 일꾼들에게 나눠 맡기는* 매커니즘. 메인 컨텍스트를 보호하고, 비용을 낮추고, 권한을 좁힌다. **하니스의 *부서 조직*** 에 해당.

> 부모 문서: [하니스 엔지니어링](../하니스-엔지니어링.md). 도구 자체 설명은 [서브에이전트](../../tools/서브에이전트.md).

## 1. 정의

Subagent = *특정 분야에 특화된 작은 Claude 인스턴스*. 각자:
- 독립된 컨텍스트 창
- 독립된 시스템 프롬프트
- 독립된 도구 화이트리스트
- 독립된 모델 (haiku / sonnet / opus 라우팅)

Delegation = 메인 에이전트가 *서브에이전트에게 작업 위임*.

## 2. 그전에는 어떤 문제가 있었나

LLM 단일 호출은 *한 컨텍스트*에서 모든 일을 처리. 큰 문제 4가지:

1. **컨텍스트 폭증**: 100개 파일 탐색 + 보안 분석 + 리팩토링을 한 세션에 → 토큰 폭발
2. **메인 오염**: 탐색 부산물(grep 결과, 파일 내용)이 메인 대화에 누적 → 핵심 결정 흐려짐
3. **권한 과잉**: 메인이 모든 도구 가져야 함 → 사고 위험
4. **비용**: 가벼운 grep 작업도 *Opus* 가 처리 → 토큰 비용 비효율

→ **분업**이 필요했다.

**일상 비유**: 회사 사장이 *영업·디자인·법무·QA*를 *동시에* 처리하려는 1인 회사 → 망함. 부서 조직 = subagent.

## 3. 위임 설계 패턴

### (A) 컨텍스트 보호 (Memory Isolation)

```text
[메인 Claude]
> "이 레포의 모든 .py 파일에서 'API_KEY' 사용 위치 찾아줘"

[Anti-Pattern] 메인이 직접 grep
  → grep 결과 1MB 가 메인 컨텍스트에 누적
  → 다음 작업에서 컨텍스트 폭발

[Pattern] Explore subagent 에 위임
  → 서브가 grep 수행
  → 메인엔 *요약*만 반환:
    "총 3곳: utils/auth.py:14, config/dev.py:8, ..."
  → 메인 컨텍스트 깨끗 유지
```

### (B) 비용 라우팅 (Model Routing)

```text
[작업의 무게에 따라 다른 모델]
파일 탐색·grep      → Haiku (빠르고 저렴)
코드 리뷰·작성     → Sonnet (균형)
아키텍처 결정·증명  → Opus (깊은 추론)

→ 같은 워크플로우 비용이 *수십 분의 1*로 떨어진다
```

### (C) 권한 분리 (Permission Boundary)

```text
agent: security-auditor
tools: [Read, Grep]  ← 읽기만
model: sonnet

agent: code-fixer
tools: [Read, Edit, Bash]  ← 수정·실행
model: sonnet

→ security-auditor 가 *코드를 수정하는 사고* 원천 차단
```

### (D) 전문성 강화 (Specialization)

각 서브에이전트는 *좁은 영역의 전문가*. 시스템 프롬프트로 깊이 있는 행동 지침 부여.

```text
agent: design-reviewer
system: "디자인 리뷰 전용. 시각적 일관성·접근성·반응형만 본다.
         코드 품질은 *논외*."
```

## Before / After

```text
[BEFORE — 단일 에이전트]
USER: "이 PR 보안·디자인·성능 다 봐줘"
AI:   [한 컨텍스트에서 다 처리]
      → 보안 점검 깊이 ↓ / 디자인 누락 / 성능 거의 무시
      → 토큰 100K, 비용 ↑↑

[AFTER — 분업]
USER: "이 PR 보안·디자인·성능 다 봐줘"
메인:   1) Agent(security-auditor) 호출 → 보안 리포트
        2) Agent(design-reviewer) 호출 → 디자인 리포트
        3) Agent(performance-checker) 호출 → 성능 리포트
        4) 메인이 *통합·요약* → 사용자에게 답변

→ 각 영역 깊이 ↑ / 메인 컨텍스트 청결 / Haiku/Sonnet 라우팅으로 비용 ↓
```

## 라이브 시연 가능한 예시

```bash
[강의 중]
> "이 레포에서 *환각* 이라는 단어가 어디 어디 등장하는지 찾아줘"

[Claude Code 출력]
🤖 Agent(Explore) 호출 중...
   서브에이전트가 grep 수행
   결과: 17곳 발견
   주요 파일: docs/phenomena/환각.md, docs/techniques/RAG.md, ...

"총 17곳에서 등장. 주요 파일 3곳 요약은 다음과 같습니다..."
```

🤖 아이콘이 뜨는 순간 = 위임이 일어나는 가시화.

## 4. Anthropic 의 *3-Agent Harness* (2026-04 발표)

장시간 자율 코딩 작업용 표준 패턴:

```text
┌─────────────────────────────────────────┐
│ Planning Agent                          │
│ "전체 작업을 phase로 쪼갠다"             │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ Generation Agent                        │
│ "각 phase의 코드를 *작성*한다"          │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ Evaluation Agent                        │
│ "Generation 결과를 *검증*한다           │
│  (별도 인스턴스가 평가해야 자만 회피)"  │
└─────────────────────────────────────────┘
```

핵심 발견 (Anthropic):
- *생성과 평가를 *같은 모델*에 시키면 자만으로 결과 부정확*
- *별도 모델·별도 시스템 프롬프트가 자기 자신을 평가하면 *2~3배* 품질 향상*

자세히는 [evaluation-loop](evaluation-loop.md).

## 한계

- **위임 자체의 비용**: 메인 → 서브 호출에도 토큰. 너무 잘게 쪼개면 *오버헤드 ↑*.
- **결과 통합의 어려움**: 3개 서브에이전트가 *충돌하는 권고*를 주면 메인이 어떻게 결합할지.
- **컨텍스트 단절**: 서브는 메인의 *전체 맥락*을 모름. 위임 시 *충분한 배경*을 같이 보내야 함.
- **MCP·서브에이전트 헷갈림**: MCP = 외부 시스템과의 표준 통로 / Subagent = 같은 모델의 분업 (자세히는 [서브에이전트](../../tools/서브에이전트.md#mcp-vs-서브에이전트--헷갈리는-두-개념)).

## 꼬리에 꼬리 (관련 개념)

- [하니스 엔지니어링](../하니스-엔지니어링.md) — 부모 문서
- [서브에이전트 (도구 측)](../../tools/서브에이전트.md) — 호출 방법·YAML 형식
- [Tools (하니스의 손)](tools.md) — 서브에이전트도 결국 도구를 쓴다
- [Evaluation Loop](evaluation-loop.md) — 3-agent 패턴의 *평가 단계*
- [Lost in the Middle](../../phenomena/Lost-in-the-Middle.md) — 분업의 *제1 이유*

## 출처

- [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — 분업·평가 패턴
- [Anthropic Designs Three-Agent Harness — InfoQ (2026-04)](https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/) — 3-agent 발표
- [Anthropic — Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents) — 위임 API
- [LangChain — Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) — 분업 디자인
