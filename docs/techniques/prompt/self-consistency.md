# Self-Consistency · Multi-Sampling

> *한 번 답에 의존하지 마라*. **같은 질문을 여러 번 보내고 *다수결로* 답을 채택**하는 패턴. [비결정성](../../phenomena/비결정성.md) 을 *오히려 활용*하는 검증 기법.

> 부모 문서: [프롬프트 엔지니어링](../프롬프트-엔지니어링.md)

## 1. 정의

Self-Consistency (Wang et al., 2022, arXiv:2203.11171):
1. 같은 프롬프트를 N번 (보통 5~40번) 모델에 보냄
2. 각 응답에서 *최종 답*만 추출
3. **가장 많이 등장한 답**을 채택 (다수결)

```text
[질문]
"100보다 작은 소수 중 7로 나누어 떨어지는 수의 개수?"

[10번 호출 결과]
1번: 1개   ← 7만 해당
2번: 1개
3번: 12개  ← 환각
4번: 1개
5번: 0개   ← 다른 환각
6번: 1개
7번: 1개
8번: 1개
9번: 14개  ← 또 다른 환각
10번: 1개

[다수결] 1개 (7회) ← 채택
```

## 2. 그전에는 어떤 문제가 있었나

LLM은 *비결정적*이다 ([비결정성](../../phenomena/비결정성.md)).
- 같은 질문 → 매번 다른 답
- 어떤 답이 *진짜인지* 알 길이 없음
- 한 번 잘 나온 답이 *우연*인지 *실력*인지 모름

→ *우연을 걸러내는 매커니즘*이 필요했다.

**일상 비유**: 일기예보가 *한 모델*만 보지 않는다. *5~10개 모델*을 동시에 돌려 *합의되는 예보*를 신뢰한다 (앙상블 예보). Self-consistency도 같은 발상.

## 3. 어떻게 작동하나

```text
1. 프롬프트 + temperature 0.3~0.7 (다양성 확보)
2. N번 호출 (병렬)
3. 답 추출 (정규표현식·구조화 파싱)
4. 다수결 투표
5. (선택) 합의도가 낮으면 *더 많이 샘플링* 또는 *모델 변경*
```

**Temperature**: 너무 낮으면 답이 비슷해서 다수결 의미 없음. 너무 높으면 답이 흩어져 다수결이 잡혀도 신뢰 낮음. *0.3~0.7* 이 sweet spot.

**N**: 5번이 최소. 복잡한 추론은 20~40번. 비용 비례.

## Before / After

```text
[BEFORE — 한 번 호출]
"이 코드의 시간 복잡도?"
→ AI: O(n²)  (= 50% 확률로 정답·50% 확률로 환각)

[AFTER — Self-consistency 5번]
호출 1: O(n²)
호출 2: O(n²)
호출 3: O(n log n)  ← 환각
호출 4: O(n²)
호출 5: O(n²)
[다수결] O(n²) (4/5)  ← 채택, 합의도 80%
```

합의도(consensus rate) 자체가 *답 신뢰도의 지표*가 된다.

## 라이브 시연 가능한 예시

```bash
[강의 중]
> "다음 시 한 줄: '봄의 비'"
호출 1: "꽃잎 위 작은 손짓"
호출 2: "메마른 땅의 첫 노래"
호출 3: "잠든 씨앗을 깨우는 속삭임"

→ 청중에게: "*비결정성*이 보이죠.
   같은 모델이 매번 다른 답."

→ 다음 시연: "100 미만 소수 중 7로 나누어지는 수 개수"
호출 5번 → 5번 모두 "1"
청중에게: "*결정적인 답*은 일관되게 나온다."

→ "이게 self-consistency. 합의도가 답 신뢰도의 지표."
```

## 4. 발전 — 검증 루프와의 결합

Self-consistency 는 *최종 답이 유일한 형태*일 때만 유효 (수치·분류·짧은 답).

복잡한 답(코드·에세이)에는 *다른 검증*이 필요:
- **Generator-Evaluator** (자세히는 [evaluation-loop](../harness/evaluation-loop.md)): 한 모델이 답하고 다른 모델이 평가
- **Cross-Model Consensus**: GPT + Claude + Gemini 가 같은 답을 하면 신뢰
- **Test-driven Verification**: 코드는 *테스트 통과* 가 가장 강한 합의

## 한계

- **비용**: N배 토큰. *짧은 답·중요한 결정* 에만 권장.
- **답 형식이 자유로우면 다수결 어려움**: *"이 코드 어때?"* 같은 자유 응답엔 부적합.
- **systematic bias**: 모델이 *체계적으로 틀리는* 영역에서는 다수결도 틀림. (예: 학습 데이터에 잘못된 정보가 많은 주제)
- **Reasoning 모델의 등장 (2026)**: o-series·Opus thinking 모드는 *내부적으로* self-consistency 비슷한 검증을 수행. 외부 N-호출 필요성 감소.

## 꼬리에 꼬리 (관련 개념)

- [프롬프트 엔지니어링](../프롬프트-엔지니어링.md) — 부모 문서
- [Chain-of-Thought](chain-of-thought.md) — Self-consistency 는 *CoT의 다수결 버전* 으로 처음 제안됨
- [비결정성](../../phenomena/비결정성.md) — 활용·극복 대상
- [Evaluation Loop](../harness/evaluation-loop.md) — 복잡한 답의 검증
- [환각](../../phenomena/환각.md) — Self-consistency 가 줄이는 핵심 대상

## 출처

- [Self-Consistency Improves Chain of Thought Reasoning (Wang et al., 2022)](https://arxiv.org/abs/2203.11171) — 원논문
- [Defeating Nondeterminism in LLM Inference (Thinking Machines, 2025-09)](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/) — 비결정성 분석
- [Anthropic — Reduce hallucinations](https://platform.claude.com/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) — Self-consistency 권장 사례
