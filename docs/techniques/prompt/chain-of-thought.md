# Chain-of-Thought (CoT) · Tree-of-Thought · Graph-of-Thought

> *"단계별로 생각해줘"* 한 줄로 정확도 30~50% 끌어올리는 추론 강화 패턴. **Chain-of-Thought**(2022, Wei et al.) 가 원전, **Tree-of-Thought**(2023) · **Graph-of-Thought**(2023) 가 비선형 확장.

> 부모 문서: [프롬프트 엔지니어링](../프롬프트-엔지니어링.md)

## 1. 정의

### Chain-of-Thought (CoT, 2022)
모델에게 *답만* 요구하지 않고 — *중간 추론 과정*을 *글로 풀어쓰게* 시킴. 그러면 정답률이 올라간다.

```text
[일반]
"5 × 7 = ?"
→ AI: "35"

[CoT]
"5 × 7 = ?  단계별로 생각해서 답해줘"
→ AI: "5를 7번 더한다.
       5+5=10, +5=15, +5=20, +5=25, +5=30, +5=35
       답: 35"
```

### Tree-of-Thought (ToT, 2023)
*선형* 사슬이 아니라 *나무 구조*로 — 여러 가설을 동시에 탐색하고 *가지치기*. 복잡한 퍼즐·전략 문제에 강함.

### Graph-of-Thought (GoT, 2023)
*나무*를 넘어 *그래프* — 사고 노드들이 *서로 결합·재사용*. 가장 복잡한 추론 구조.

## 2. 그전에는 어떤 문제가 있었나

GPT-3 시대(2020) — 모델이 *수학·논리 문제*에서 자주 틀렸다.

- 단순 산수: *"23 × 47 = ?"* → 자주 틀림
- 단어 문제: *"사과 5개를 3명에게 나눠주면..."* → 첫 직감으로 답하다 실수
- 다단계 추론이 필요한 문제 → 거의 불가

→ 모델이 *시간을 들여 생각하게* 하는 매커니즘이 없었다.

**일상 비유**: 시험 문제를 *암산*만으로 풀려는 학생. *연필로 풀이 과정을 쓰면* 정답률이 올라가는 것과 같은 일이 LLM에서도 일어난다.

## 3. 원전 — Wei et al. 2022

논문: *"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"* (arXiv:2201.11903, Google Brain)

핵심 발견:
- *Few-shot CoT*: 예시 안에 *중간 추론 과정*을 넣음 → 수학 정확도 17% → **57%** (PaLM 540B 기준).
- *Zero-shot CoT* (Kojima et al., 2022): *"Let's think step by step"* 한 줄만 추가해도 큰 효과.
- *모델 크기에 비례*: 작은 모델은 효과 적음. 100B+ 파라미터에서 emergent.

## Before / After

### 단어 문제

```text
[CoT 없음]
"체육관에 농구공 23개와 야구공 7박스(박스당 12개)가 있다. 총 몇 개?"
→ AI: "30개"  (= 박스를 세기 빼먹음)

[CoT]
"체육관에 농구공 23개와 야구공 7박스(박스당 12개)가 있다. 총 몇 개?
 단계별로 생각해서 답해줘."
→ AI: "1) 농구공: 23개
       2) 야구공: 7 × 12 = 84개
       3) 총: 23 + 84 = 107개
       답: 107"
```

### 코드 디버깅

```text
[CoT 없음]
"이 코드 왜 안 되지?  def f(x): return x*2; print(f([1,2,3]))"
→ AI: "f가 리스트를 곱하기 때문입니다."  (= 모호)

[CoT]
"이 코드 왜 안 되지? 단계별로 분석해줘.
 def f(x): return x*2; print(f([1,2,3]))"
→ AI: "1) print(f([1,2,3])) 호출
       2) f 안에서 x = [1,2,3]
       3) x * 2 → [1,2,3] * 2 → [1,2,3,1,2,3]
          (= 리스트 반복, 사용자가 의도한 것과 다름)
       4) 사용자 의도: 각 원소를 2배 → [2,4,6]
       5) 해결: return [i*2 for i in x]"
```

## 라이브 시연 가능한 예시

가장 강력한 한 장 — *같은 모델, 한 줄 추가만으로 답이 달라진다*.

```bash
[화면 A]
> "100보다 작은 소수 중 7로 나누어 떨어지는 수의 개수?"
→ AI: "12개" (자주 틀림)

[화면 B — "단계별로" 한 줄 추가]
> "100보다 작은 소수 중 7로 나누어 떨어지는 수의 개수? 단계별로 생각해서 답해줘"
→ AI: "1) 소수는 1과 자기 자신으로만 나뉨
       2) 7로 나누어 떨어진다 = 7의 배수
       3) 7의 배수 중 *소수*는 → 7 자신뿐
       4) 답: 1개"
```

청중에게: *"한 줄을 추가했을 뿐인데 — 답이 *틀린 답에서 정답*으로."*

## Tree-of-Thought · Graph-of-Thought (간단)

복잡한 문제용 확장.

| 패턴 | 사고 구조 | 적합한 문제 |
|---|---|---|
| **CoT** | 직선 | 산수·단순 추론 |
| **ToT** | 나무 (가설 분기) | 퍼즐·게임·전략 |
| **GoT** | 그래프 (재사용) | 대규모 계획·증명 |

ToT 예시: 24 게임 (4개 숫자로 24 만들기). 모델이 *여러 가설*을 동시에 시도하고 *틀린 가지를 가지치기*.

```text
[ToT]
"숫자 4, 9, 10, 13으로 24를 만들어"
→ 가설1: 4 + 9 + 10 = 23 ❌ (가지치기)
→ 가설2: 13 - 9 = 4, 4 × 10 / 4 = 10 ❌
→ 가설3: 10 - 4 = 6, 6 × (13 - 9) = 24 ✓
```

## 한계

- **CoT는 *쓸데없이 길어짐***: *"안녕"* 같은 단순 질문에 step-by-step 시키면 이상한 답.
- **거짓 추론**: 추론은 자연스러워 보이지만 *결론이 틀린* 사례 — 환각의 한 형태.
- **비용**: 토큰 사용량 ↑ → 비용 ↑.
- **2026 reasoning 모델 (o-series·Claude Opus thinking)**: CoT가 *모델 내장*. 사용자가 명시적 지시 안 해도 됨.

## 꼬리에 꼬리 (관련 개념)

- [프롬프트 엔지니어링](../프롬프트-엔지니어링.md) — 부모 문서
- [Zero/Few-shot](zero-few-shot.md) — Few-shot CoT는 가장 강력한 결합
- [Self-Consistency](self-consistency.md) — CoT를 *여러 번 돌려 다수결* 패턴
- [Meta-Prompting](meta-prompting.md) — *어떤 CoT 가 필요한지* 모델이 스스로 결정
- [환각](../../phenomena/환각.md) — *그럴듯한 거짓 추론* 위험

## 출처

- [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903) — 원논문
- [Large Language Models are Zero-Shot Reasoners (Kojima et al., 2022)](https://arxiv.org/abs/2205.11916) — Zero-shot CoT 발견
- [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601) — ToT 원전
- [Graph of Thoughts (Besta et al., 2023)](https://arxiv.org/abs/2308.09687) — GoT 원전
- [Prompting Guide — Chain-of-Thought](https://www.promptingguide.ai/techniques/cot) — 종합
