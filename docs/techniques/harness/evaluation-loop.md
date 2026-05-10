# Evaluation Loop (검증 루프)

> 모델이 만든 것을 *모델이 자기 검증*하지 않고, **별도 매커니즘**이 검증하는 루프. Anthropic 권고: *"Separate generation from evaluation"*. **하니스의 *심판***.

> 부모 문서: [하니스 엔지니어링](../하니스-엔지니어링.md)

## 1. 정의

Evaluation Loop = 모델 출력을 *받아 검증하고·실패 시 다시 시도하게* 만드는 자동화된 루프.

```text
[1] 모델이 결과 생성
       ↓
[2] *별도 검증기*가 평가
       ↓
[3] 통과? → 끝.   실패? → 피드백과 함께 [1]로 다시.
```

핵심: **검증기가 *별도*** 여야 한다. 같은 모델이 자기 답을 채점하면 — *자만으로 통과*.

## 2. 그전에는 어떤 문제가 있었나

LLM이 *코드 짜고·자기가 평가*하면:

- *"이 코드 어때?"* → AI: "좋아요. 통과." (= 거의 항상 자기 자랑)
- 진짜 결함이 있어도 *못 잡음*
- 사용자가 결국 *직접 검증* — 자동화 의미 사라짐

→ *외부 심판*이 필요했다.

**일상 비유**: 학생이 *자기 시험을 자기가 채점*하면 — 객관성 ❌. 별도 채점관이 필요한 이유.

## 3. 세 가지 검증 방식 (Anthropic 권고)

### (A) Rules-based (규칙 기반)
*결정론적* 도구로 검증. 가장 신뢰성 높음.

```text
- 테스트 통과 (pytest, npm test)
- 린터 통과 (ruff, eslint)
- 타입 체커 (mypy, tsc)
- 컴파일 성공
- 정규식 패턴 매칭
```

**장점**: 100% 객관적·결정적
**한계**: *규칙으로 표현 가능한* 것만 검증

### (B) Visual (시각 기반)
UI 작업에서 *스크린샷·비교*로 검증.

```text
- Playwright 로 스크린샷 → 모델이 "디자인 시안과 일치하나" 평가
- 픽셀 diff → 변화 영역 표시
- 접근성 자동 점검 (axe, Lighthouse)
```

**장점**: UI 결함을 *사람이 보기 전에* 잡음
**한계**: 미묘한 *디자인 감각*은 모델도 놓침

### (C) LLM-as-Judge (LLM 심판)
*다른 모델·다른 시스템 프롬프트*가 평가.

```text
[Generator] 모델 A: 답변 작성
[Judge]     모델 B: "답변 A를 *정확성·완결성·톤* 기준으로 채점"
[결과]      점수 7/10. 부족 부분: 톤이 너무 격식.
[다시]      Generator 가 톤 수정 후 재생성
```

**장점**: 자유 응답·창의적 작업에 적용 가능
**한계**: Judge 도 모델이라 *환각·편향* 가능. 그러나 *생성과 분리*하는 것만으로도 큰 효과.

### Anthropic 정량적 효과
*"검증 없이 vs 검증 루프* 적용 시 — **2~3배 품질 향상** (코딩 벤치마크 기준).

## Before / After

```text
[BEFORE — 자가 검증]
Generator: "코드 짰어요"
Self-eval: "잘 됐어요"
사용자: (실행 → 빌드 실패)
사용자: "안 되는데?"
Generator: "수정했어요"
사용자: (실행 → 또 실패)
        ...

[AFTER — Rules-based 검증 루프]
Generator: "코드 짰어요"
Auto: pytest 실행 → 3 fail
Generator: 실패 결과 보고 수정
Auto: pytest 재실행 → all pass
Generator: "완료" (= 사람 개입 없이 통과)
```

## 라이브 시연 가능한 예시

```bash
[강의 중 — Claude Code]
> "Python 피보나치 짜고 테스트도 통과시켜줘"

[Claude의 evaluation loop]
🔧 Write fib.py
🔧 Write test_fib.py
🔧 Bash: pytest
   결과: FAILED: fib(0) returned 1, expected 0
🔧 Edit fib.py (base case 수정)
🔧 Bash: pytest
   결과: PASSED 5/5 ✓
"완료. 모든 테스트 통과."
```

청중에게: *"AI가 자기 코드를 자기가 돌리고 자기가 고친다"* — 검증 루프가 자동화한 *반복*.

## 4. 실제 사례 (2026)

### Anthropic 의 *3-Agent Harness*
- Plan agent → Generate agent → **Evaluate agent**
- Evaluate agent 가 *별도 모델*로 작동, 자만 회피

### Claude Code 의 `tdd-guard` hook
- `PreToolUse` 에 등록 → 코드 변경 *직전*에 *대응 테스트가 있는지* 자동 점검
- 없으면 차단 + *"테스트 먼저 짜라"* 메시지 (자세히는 [Hooks](../../tools/Claude-Code-Hooks.md))

### oh-my-claudecode 의 `team-verify`
- 5단계 자동 파이프라인의 4번째 — `team-plan → team-prd → team-exec → team-verify → team-fix`
- *team-verify* 가 *team-exec* 결과를 별도로 평가

### Generator-Evaluator GAN-style
- 두 에이전트가 *적대적*으로 작동 — Generator는 만들고, Evaluator는 결함을 찾고
- 결함 → Generator 수정 → 결함 없을 때까지 반복

## 한계

- **무한 루프 위험**: Evaluator 가 *불가능한 기준*을 요구하면 영원히 맴돔. *최대 시도 횟수* 설정 필수.
- **Judge 의 편향**: LLM-as-Judge 도 결국 모델. *체계적 편향* 위험. Cross-check 필요.
- **비용**: 매 시도마다 토큰 ↑. *복잡한 작업*에만 권장.
- **Rules 부재**: 자유 응답·창의 작업은 *rules-based 가 어려움*. 결국 사람의 마지막 검토 필요.

## 꼬리에 꼬리 (관련 개념)

- [하니스 엔지니어링](../하니스-엔지니어링.md) — 부모 문서
- [서브에이전트와 분업](subagents-and-delegation.md) — Generator-Evaluator 의 분업 패턴
- [Tools (하니스의 손)](tools.md) — 검증 도구(테스트·린터)도 결국 tools
- [퍼미션·훅](permissions-and-hooks.md) — Hook 으로 *결정론적 검증* 자동 발화
- [Self-Consistency](../prompt/self-consistency.md) — 검증의 *프롬프트 측* 패턴
- [비결정성](../../phenomena/비결정성.md) — 검증이 *비결정성을 잡는* 매커니즘
- [환각](../../phenomena/환각.md) — 검증이 *환각을 잡는* 매커니즘
- [TDD](../TDD.md) — 검증 게이트의 *코드 단위 표준 구현*

## 출처

- [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — 3-agent 권고
- [Anthropic Three-Agent Harness — InfoQ (2026-04)](https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/) — 발표 정리
- [HumanLayer — Skill Issue: Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) — 검증 디자인 패턴
