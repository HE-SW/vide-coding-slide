# Agentic Engineering (에이전틱 엔지니어링)

> *바이브코딩의 진화형*. 한 번 던지고 받아보는 *프롬프트 코딩*에서 — *계획·실행·검증을 자율적으로 도는 에이전트 워크플로우* 로의 전환. **2026년 5월 Karpathy 가 Sequoia AI Ascent에서 공식 선언한 패러다임 이동**. 강의 전반의 메시지가 *2026 시점에서 어떻게 진화*했는가의 답.

## 1. 왜 "Agentic Engineering"이라고 부르나

- **Agentic(에이전트적인) + Engineering**. *"에이전트가 자율적으로 일하지만, *엔지니어링 규율* 안에서"* 라는 두 단어의 결합.
- **공식 데뷔**: 2026년 5월, **Andrej Karpathy** 가 Sequoia *AI Ascent 2026* 에서 fireside chat 으로 발표. 발표 제목이 정확히 *"From Vibe Coding to Agentic Engineering"*.
- 2025-12 시점이 Karpathy 본인의 *변곡점*: *"11월에 80% 직접 코드를 짰는데, 12월에 80% AI 에 위임했다"*.
- **2026년 한 해의 핵심 키워드** — 바이브코딩의 *직접적 후계*.

## 2. 그전에는 어떤 문제가 있었나 — 바이브코딩의 한계

[바이브코딩](바이브코딩.md) (2025-02 Karpathy 명명)은 강력했지만 *프로덕션 스케일*에서 무너졌다.

```text
바이브코딩의 약점 (2025년 후반에 드러남):
  ❌ 디자인 단계 *스킵*
  ❌ 리뷰 단계 *스킵*
  ❌ 테스트 단계 *스킵*
  ❌ 보안·확장성·실사용자 부담 *고려 못 함*

  → 데모는 잘 됨. 프로덕션은 무너짐.
  → "raise the floor for everyone" (모두가 시작 가능) 은 OK
  → 그러나 "preserve the quality bar" (전문 품질 유지) 는 ❌
```

→ *전문 소프트웨어의 품질 기준*은 지키면서 *AI 가속*도 받는 매커니즘이 필요했다.

**일상 비유**: 자전거 보조 바퀴를 떼고 자전거를 *잘* 타려는 단계. 바이브코딩 = *보조 바퀴 자전거* (누구나 굴릴 수 있음). Agentic engineering = *제대로 타기* (속도·안전·거리 다 챙김).

## 3. 어떻게 해결했나 — 핵심 3가지

### (A) Karpathy 의 정의

> *"Agentic engineering is an engineering discipline where agents are spiky entities — fallible and stochastic, but extremely powerful — coordinated to go faster without sacrificing quality."*

**핵심 단어**:
- **Spiky** (뾰족함) — AI 는 *어떤 영역에서는 천재, 어떤 영역에서는 바보*. 균등하게 똑똑하지 않음
- **Fallible · Stochastic** — 잘못한다 + 매번 다르다 ([환각](../phenomena/환각.md) + [비결정성](../phenomena/비결정성.md))
- **Coordinated** — 그래서 *지휘 매커니즘* 필요 ([Orchestration](../techniques/Orchestration.md))
- **Without sacrificing quality** — 속도와 품질 *둘 다*

### (B) PEV Loop — Plan, Execute, Verify

agentic engineering 의 *코어 워크플로우*:

```text
┌──────────┐     ┌──────────┐     ┌──────────┐
│   Plan   │ →   │ Execute  │ →   │  Verify  │
│ (계획)    │     │ (실행)    │     │ (검증)    │
└──────────┘     └──────────┘     └────┬─────┘
                                        │
       ↑                                │
       └────── 실패 시 다시 ───────────┘
```

- **Plan** — 사용자 요구를 *명세화* + *Phase 분할*
- **Execute** — 실제 코드 작성·도구 호출·테스트 실행
- **Verify** — 결과 검증. 실패 시 Plan 으로 복귀

→ "프롬프트 한 번 던지고 끝" → "계획-실행-검증의 *자율 루프*".

### (C) Spec-Driven Development — Agentic 의 동반자

*"명세가 1차 산출물"* 이라는 발상. 코드보다 *명세*가 먼저, 코드는 명세에서 자동 도출.

```text
[Vibe Coding]
의도 → 코드

[Agentic Engineering]
의도 → 명세(spec) → AI 계획 → 코드 + 테스트 + 리뷰
                  │
                  └─ 명세가 모호하면 AI가 사용자에게 *clarify* 요청
```

명세가 *판단을 위임받는 AI 의 가드레일*. AI 가 *추측해서 채우는* 영역을 줄임 → 환각·잘못된 가정 회피.

## Before / After — Karpathy 자신의 1년

```text
[2025-11 Karpathy]
- 80% 본인 직접 코드 작성
- 20% AI 보조

[2025-12 변곡점]
"agent capability 가 *임계점* 을 넘었다"

[2026-05 Karpathy]
- 80% AI 가 작성·실행·검증
- 20% 본인 = *판단·취향·감독*

→ "You can outsource thinking. You can't outsource understanding."
   (생각은 위임할 수 있어도, 이해는 위임할 수 없다)
```

이 한 줄이 강의 메시지와 *직접 연결*. 비개발자도 *결정·이해의 주체*로 남는다.

## 라이브 시연 가능한 예시

### 시연 — Vibe vs Agentic 같은 작업
```bash
[Vibe Coding 식]
> "TODO 앱 만들어줘"
→ AI: 코드 한 덩어리 출력 (50줄)
사용자: 직접 실행 → 에러 → "이 부분 수정해줘"
→ AI: 다른 50줄
... 반복 → 30분 후 *동작은 함, 테스트 없음, 리팩토링 안 됨*

[Agentic Engineering 식 — `/harness`]
> "/harness  TODO 앱 만들어줘"
→ AI:
  Plan: PRD 작성 (5분, 사용자 검토)
  Execute: Phase 1~5 자동 (10분)
    each: 코드 + 테스트 + 자동 커밋
  Verify: 모든 phase 의 통합 테스트
→ 17분 후 *동작 + 테스트 통과 + 리팩토링 + 문서화*
```

청중에게: *"같은 모델·같은 사용자 — *워크플로우*가 결과를 결정한다."*

## 4. Agentic Engineering 의 7대 특징 (2026 업계 합의)

| 특징 | 설명 |
|---|---|
| **Spec-First** | 명세가 1차 산출물. 코드는 명세에서 도출 |
| **PEV Loop** | Plan-Execute-Verify 의 자율 반복 |
| **Multi-Agent** | 분업 (author·tester·reviewer·security 등) |
| **Tool Use** | 모델이 도구를 호출해 *행동* (자세히는 [Tool Use](Tool-Use.md)) |
| **HITL Checkpoints** | 결정적 순간에 사람 승인 (자세히는 [HITL](Human-in-the-Loop.md)) |
| **Verifiable Goals** | "버그 고쳐줘" → "테스트 통과시켜라" |
| **Quality Gates** | 단계마다 *통과 기준* 명시 (린트·테스트·검토) |

## 5. 강의 연결 포인트 — 가장 중요한 메시지 업데이트

### 강의 메시지 진화

```text
초기 강의 메시지 (2025년 시점):
  "좋은 결과는 우연이 아니라 설계"
  "User → Orchestrator"
  "프롬프트 + 컨텍스트 + 하니스 3축"

기존 메시지 + Agentic Engineering (2026 진화):
  → "좋은 결과 = Plan-Execute-Verify 루프"
  → "사람은 *생각·이해의 주체*, AI 는 *실행·검증의 가속기*"
  → "3축 + Spec-driven + HITL = Agentic Engineering"
```

### *2층 하니스* 와의 관계

강의에서 가르친 *CLAUDE.md + docs + skills + hooks* 4 레이어 = **Agentic Engineering 의 *재료들***. 이걸 *어떻게 흐르게 할 것인가* 가 PEV 루프.

→ **하니스 세팅 = Agentic Engineering 의 *세팅편*. 이후 강의의 *Dicom Viewer 만들기* = *실전편***.

## 한계와 비판

- **"vibe coding 의 자리는 여전히 있다"** — Simon Willison(2026-05): *"두 진영은 *겹치고* 있다"*. 빠른 프로토타입엔 vibe, 프로덕션엔 agentic. *둘 다*.
- **명세의 비용**: spec-driven 의 명세 자체가 *시간·노력*. 모든 작업에 적용 ❌. 1회용 스크립트는 vibe 가 적합.
- **"진짜 *이해*가 줄어든다"** 우려: AI 위임 80% → 사람의 *코드 이해도*는? Karpathy 본인도 *"내가 짠 게 아닌 코드가 늘어나면 디버그가 어렵다"* 인정.
- **2026 vs 미래**: 이 표현 자체도 *바이브코딩의 진화* — 2027~2028년에 또 다른 이름이 나올 수 있다.

## 꼬리에 꼬리 (관련 개념)

- [바이브코딩](바이브코딩.md) — 직전 패러다임. 부모 격
- [Andrej Karpathy](../people/Andrej-Karpathy.md) — Vibe coding 명명자 + Agentic engineering 선언자
- [LLM](LLM.md) / [Tool Use](Tool-Use.md) — Agentic 의 기술 토대
- [Human-in-the-Loop](Human-in-the-Loop.md) — Agentic 의 *사람 개입 매커니즘*
- [AI Adoption Spectrum](AI-Adoption-Spectrum.md) — AI-native 단계의 표준 워크플로우
- [Orchestration](../techniques/Orchestration.md) — Agentic 의 *지휘 매커니즘*
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — Agentic 의 *작업 환경 설계*
- [하이퍼-워터폴](../methodologies/하이퍼-워터폴.md) — Agentic 의 *방법론적 구현 사례*
- [문서 주도 개발](../techniques/문서-주도-개발.md) — Spec-driven 의 *마크다운 구현*
- [Evaluation Loop](../techniques/harness/evaluation-loop.md) — PEV 의 *Verify 단계*

## 출처

- [Karpathy — Sequoia Ascent 2026 summary (bearblog)](https://karpathy.bearblog.dev/sequoia-ascent-2026/) — 본인 발표 요약 1차 자료
- [YouTube — Andrej Karpathy: From Vibe Coding to Agentic Engineering](https://www.youtube.com/watch?v=96jN2OCOfLs) — 발표 영상
- [AIntelligenceHub — Karpathy: AI Coding Moving From Vibe Prompts to Agent Workflows (2026-05)](https://aintelligencehub.com/articles/karpathy-vibe-coding-to-agent-workflows-may-2026) — 발표 분석
- [Analytics Drift — Karpathy Declares Vibe Coding Obsolete, Introduces Agentic Engineering](https://analyticsdrift.com/andrej-karpathy-agentic-engineering-software-3/) — 산업 반응
- [Adnan Masood — You Can Outsource Thinking. You Can't Outsource Understanding (Medium, 2026-05)](https://medium.com/@adnanmasood/you-can-outsource-thinking-you-cant-outsource-understanding-fd02f1994e02) — 핵심 인용 분석
- [Simon Willison — Vibe coding and agentic engineering are getting closer than I'd like (2026-05-06)](https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/) — 균형잡힌 비평
- [InterCode — Vibe Coding vs. Spec-Driven Development in 2026](https://intercode.com/blog/vibe-coding-vs-spec-driven-development-in-2026) — Spec-driven 비교
- [NxCode — Agentic Engineering Complete Guide (2026)](https://www.nxcode.io/resources/news/agentic-engineering-complete-guide-vibe-coding-ai-agents-2026) — PEV loop 정리
- [DEV Community — Why Agentic Engineering Must Replace Vibe Coding](https://dev.to/shrsv/why-agentic-engineering-must-replace-vibe-coding-339f) — 강한 입장
- [TATEEDA — Vibe Coding vs. Engineering: A 2026 Guide](https://tateeda.com/blog/vibe-coding-vs-professional-engineering) — 트레이드오프
- [Vibe coding — Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding) — 정의·역사
