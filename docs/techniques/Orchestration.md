# Orchestration (오케스트레이션)

> 여러 AI 에이전트·도구·단계를 *지휘하는* 매커니즘. *어떤 일을·어느 순서로·어떤 일꾼이·어떻게 합쳐* 진행할지 결정. **하니스의 *지휘자***. 2026년 LangGraph·Claude Agent SDK·OpenAI Agents SDK·Strands 4대 프레임워크가 표준화.

## 1. 왜 "오케스트레이션"이라고 부르나

- **Orchestra(오케스트라) + ation**. *지휘자가 다양한 악기를 조화시킨다*는 비유.
- 컴퓨팅에서 오래 쓴 단어 — *Kubernetes 가 컨테이너 오케스트레이션*, *Airflow 가 워크플로우 오케스트레이션*.
- AI 시대에 와서 *멀티 에이전트 + 도구 + 사람 검토* 를 조율하는 매커니즘으로 의미 확장.
- **2026 표준**: LangGraph (47M 월 다운로드, 가장 큰 채택), Claude Agent SDK, OpenAI Agents SDK, Strands (AWS) — 4대 프레임워크가 시장 형성.

## 2. 그전에는 어떤 문제가 있었나

단일 에이전트·단일 LLM 호출로 *복잡한 워크플로우*를 못 다룬다.

- 책 한 권 쓰기·대규모 코드베이스 리팩토링 → 한 호출에 불가능
- 여러 *전문 에이전트*가 협력해야 → *누가 언제 무엇을 하나* 결정 필요
- *상태가 단계 사이를 흘러야* → 메모리·체크포인트 설계 필요
- *사람의 개입 시점* → 어디에 끼울지 결정

→ *지휘자 추상화*가 필요했다.

**일상 비유**: 큰 영화 제작. *감독·시나리오·배우·촬영·편집·음향·VFX* 모두 따로 일하면 영화가 안 만들어짐. *프로듀서/조감독*이 *전체 흐름*을 조율한다. 오케스트레이션 = *그 프로듀서 역할*.

## 3. 4대 프레임워크 (2026)

```text
┌─────────────────────────────────────────────────────────────────┐
│                    AI Agent Orchestration 2026                  │
├──────────────────┬──────────────────────────────────────────────┤
│ LangGraph        │ 47M 월다운로드. 가장 큰 채택. 그래프 기반,     │
│ (LangChain)      │ 명시적 상태, HITL `interrupt()` 표준          │
├──────────────────┼──────────────────────────────────────────────┤
│ Claude Agent SDK │ Anthropic 공식. Tools/hooks/MCP/skills 통합.  │
│ (Anthropic)      │ 2026-05 *dreaming* + 20-parallel 발표         │
├──────────────────┼──────────────────────────────────────────────┤
│ OpenAI Agents    │ OpenAI 공식. *Apps SDK·Connectors* 통합.       │
│ SDK              │ ChatGPT 생태계와 강한 결합                    │
├──────────────────┼──────────────────────────────────────────────┤
│ Strands Agents   │ AWS 공식. Bedrock·Vertex 같은 클라우드 통합. │
│ (AWS)            │ Enterprise 채택 빠름                          │
└──────────────────┴──────────────────────────────────────────────┘
```

각 프레임워크는 *서로 다른 우선순위*. 같은 멀티에이전트 작업을 4가지 다른 디자인으로 푼다.

## 4. 오케스트레이션 4 패턴

### (A) Orchestrator-Worker (지휘자-일꾼)
```text
┌──────────────┐
│ Orchestrator │  계획·분배·통합
└──────┬───────┘
       ├──── Worker 1 (탐색)
       ├──── Worker 2 (분석)
       └──── Worker 3 (작성)
```
- *서브태스크가 사전 정의 안 됨* — 동적으로 위임
- 코드 작성·문서 통합처럼 *지휘 결정이 매번 다른* 작업에 적합
- LangGraph 의 `Send API` 가 표준 매커니즘

### (B) Sequential (순차)
```text
A → B → C → D
```
- 의존성이 명확할 때
- 우리 강의의 `/harness` 5단계 = sequential

### (C) Parallel (병렬)
```text
A ─┐
B ─┼──→ Combine
C ─┘
```
- 독립적인 작업 동시 실행
- Anthropic 2026-05 발표: *최대 20개 specialist 병렬*
- 워크트리 격리 필수

### (D) Evaluator-Optimizer (평가-최적화)
```text
Generator → Evaluator
   ↑           ↓
   └── feedback ──┘ (반복)
```
- Generator 가 만들고 Evaluator 가 채점·재시도 요청
- Anthropic *3-Agent Harness* (Plan + Generate + Evaluate)
- 자세히는 [Evaluation Loop](harness/evaluation-loop.md)

## Before / After

```text
[BEFORE — 단일 에이전트]
USER: "이 레포 보안 점검·UI 리뷰·성능 분석해줘"
AI:   [한 컨텍스트에서 다 처리]
      → 깊이 ↓ / 토큰 100K / 답변 흐릿

[AFTER — Orchestrator-Worker]
Orchestrator: "3가지 영역. 병렬 분배"
  Worker[security]   → 보안 리포트 (Sonnet)
  Worker[design]     → 디자인 리포트 (Sonnet)
  Worker[performance]→ 성능 리포트 (Haiku, 저렴)
Orchestrator: "3개 리포트 통합 → 우선순위 점검"
  → 사용자에게 통합 답변

→ 각 영역 깊이 ↑ / 비용 ↓ / 메인 컨텍스트 청결
```

## 라이브 시연 가능한 예시

### 시연 — `/harness` 의 오케스트레이션
```bash
[강의 중]
> /harness

[Orchestration 가시화]
Phase 1: claude -p (Sonnet) → working/phase-1.md
Phase 2: claude -p (Sonnet) → working/phase-2.md  ← 직렬
Phase 3: claude -p (Haiku) → working/phase-3.md   ← 모델 라우팅
Phase 4: [parallel] claude -p × 3                ← 병렬
Phase 5: claude -p + evaluator                   ← 평가-최적화

→ 17분 후 통합
```
청중에게: *"`/harness` 한 줄이 사실은 *5단계 오케스트레이션*"*.

## 5. Anthropic 의 2026-05 *Code with Claude* 발표

### Dreaming (꿈꾸기)
*백그라운드에서 자율적으로 진행되는 작업*. 사용자가 잠든 사이에도 에이전트가 *주기적 tick*으로 깨어나 작업.

```text
[잠자기 전]
> "내일 아침까지 이 PR들 다 리뷰해줘"

[밤 사이]
- 30분마다 자동 깨움
- PR 1개씩 리뷰
- 작성 결과를 메인 큐에 저장

[아침]
사용자: "결과 줘"
→ 12개 PR 리뷰 완료, 우선 처리 3건 표시
```

### Multi-agent Orchestration up to 20 Parallel Specialists
*최대 20개 전문 에이전트* 가 동시에 일하는 표준 매커니즘. 각자 독립 컨텍스트·도구·모델.

→ AI-native 시대의 *팀 단위 자동화*가 표준이 됨.

## 6. Orchestration 과 다른 개념의 관계

| 개념 | Orchestration 과의 관계 |
|---|---|
| **MCP** | Orchestration 이 *외부 도구*를 호출할 때 표준 통로 |
| **Subagents** | Orchestration 의 *worker*. 위임 대상 |
| **Hooks** | Orchestration 의 *체크포인트* (PreToolUse, Stop) |
| **HITL** | Orchestration 의 *사람 개입 지점* (`interrupt()`) |
| **하니스 엔지니어링** | Orchestration 의 *상위 추상화*. 하니스 = *모든 모델 외부 코드*, Orchestration = *그 안의 흐름 지휘* |

## 한계와 주의

- **단일 에이전트가 더 나을 때**: 작업이 *작고 단순*하면 orchestration 자체의 오버헤드가 비용 ↑.
- **상태 폭증**: 많은 에이전트가 *각자 결과물*을 누적 → 통합 컨텍스트 폭발.
- **디버깅 어려움**: 5단계 실패 시 *어느 단계가 원인인지* 추적 어려움. 관측성·로깅 필수.
- **충돌하는 권고**: 여러 worker 가 *서로 모순되는* 결과를 줄 때 — orchestrator 가 어떻게 결정할지 설계 필요.

## 강의 연결 포인트

- **"User → Orchestrator" 메시지** — 정확히 이 문서의 본문. 사용자가 *지휘자* 위치로 이동하면 — *AI 에이전트들이 그 아래 일꾼*.
- **`/harness` 5단계 흐름 슬라이드** — orchestration 의 *살아있는 사례*.
- **1층+2층 통합 그림** [데모: 16-two-layers-combined.html] — orchestration 이 그 *위에서 흐르는* 매커니즘.
- **이후 강의 (예고)** — *Dicom Viewer 만들기* 5단계 워크플로우 = orchestration 의 *실전 체화*.

## 꼬리에 꼬리 (관련 개념)

- [하니스 엔지니어링](하니스-엔지니어링.md) — Orchestration 의 *상위 추상화*
- [Subagents & Delegation](harness/subagents-and-delegation.md) — Orchestration 의 *분업 매커니즘*
- [Evaluation Loop](harness/evaluation-loop.md) — Evaluator-Optimizer 패턴 deep dive
- [Control & State](harness/control-and-state.md) — Phase 분할 + 상태 영속화
- [Permissions & Hooks](harness/permissions-and-hooks.md) — Orchestration 안의 안전장치
- [Human-in-the-Loop](../concepts/Human-in-the-Loop.md) — Orchestration 의 *사람 개입 지점*
- [MCP](../tools/MCP.md) — Orchestration 의 *외부 도구 통로*
- [Claude Code Headless 모드](../tools/Claude-Code-Headless-모드.md) — Orchestration 의 *프로그래밍 호출*

## 출처

- [Anthropic — Building Effective AI Agents (2024-12)](https://resources.anthropic.com/building-effective-ai-agents) — 4 패턴 원전
- [Anthropic — Building Effective AI Agents PDF (2026 update)](https://resources.anthropic.com/hubfs/Building%20Effective%20AI%20Agents-%20Architecture%20Patterns%20and%20Implementation%20Frameworks.pdf) — 2026 갱신본
- [LangChain — Workflows and agents (LangGraph Docs)](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — orchestrator-worker 표준
- [QubitTool — 2026 AI Agent Framework Showdown](https://qubittool.com/blog/ai-agent-framework-comparison-2026) — 4대 프레임워크 비교
- [Build Fast With AI — Claude Managed Agents Dreaming Explained (2026)](https://www.buildfastwithai.com/blogs/claude-managed-agents-dreaming-explained) — 2026-05 발표
- [Adopt.ai — Multi-Agent Frameworks for Enterprise (2026)](https://www.adopt.ai/blog/multi-agent-frameworks) — 엔터프라이즈 채택 분석
- [TechBytes — LangGraph + MCP: Multi-Agent Workflows (2026)](https://techbytes.app/posts/langgraph-mcp-multi-agent-workflow-guide-2026/) — LangGraph + MCP 통합
- [Alice Labs — AI Agent Frameworks 2026 Production Ranking](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026) — 프로덕션 채택 평가
