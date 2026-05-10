# Zero-shot · One-shot · Few-shot 프롬프팅

> *예시를 몇 개나 줄 것인가*. 0개 / 1개 / 2~5개. **프롬프트 엔지니어링의 가장 기본**이자 첫 분기점.

> 부모 문서: [프롬프트 엔지니어링](../프롬프트-엔지니어링.md)

## 1. 정의

```text
Zero-shot   : "이 문장 영어로 번역해줘"
              ─ 예시 없음. 지시문만.

One-shot    : "'안녕'→'Hello'.  '잘가'는?"
              ─ 예시 1개.

Few-shot    : "'안녕'→'Hello'
               '감사'→'Thank you'
               '잘가'→?"
              ─ 예시 2~5개. 패턴을 모델이 잡게 함.
```

## 2. 그전에는 어떤 문제가 있었나

GPT-3 이전(2020 이전) — 모델은 *명시적 예시 없이*는 새 패턴을 배우기 어려웠다.

- *번역기를 만들려면* 수만 개 영어-한국어 페어를 *학습*시켜야 했다 (파인튜닝)
- 매 새 작업마다 *모델 재학습*. 비용 ↑↑↑

→ GPT-3 가 *In-Context Learning* 능력을 보이며 — 학습 없이 *프롬프트의 예시*만으로 패턴 학습이 가능해졌다.

**일상 비유**: 새 알바생에게 *"이렇게 정리해줘"* 라고 *예시 한두 개*만 보여주면 — 별도 교육 없이 같은 식으로 일한다. Few-shot이 정확히 그 발상.

## 3. 언제 무엇을 쓰나

| 상황 | 권장 |
|---|---|
| 작업이 **일반적**·예시 만들기 어려움 | **Zero-shot** |
| 작업 양식이 *조금 특이*함 | **One-shot** (예시 1개로 양식 잡기) |
| 작업이 **좁고 양식 엄격** (분류·추출·구조화) | **Few-shot** (3개 권장) |
| 추론이 핵심 | Zero-shot + [Chain-of-Thought](chain-of-thought.md) |
| 매우 복잡 | Few-shot + CoT 결합 |

## Before / After

### 분류 작업

```text
[Zero-shot]
USER: "다음 리뷰의 감성: '비 오는 날인데 따뜻하다'"
AI:   "긍정적인 감성으로 보입니다."  (모호한 응답)

[Few-shot — 양식 강제]
USER: "감성 분류:
       '오늘 하늘이 맑다'   → 긍정
       '시험 또 망쳤어'     → 부정
       '음식이 평범해'      → 중립

       '비 오는 날인데 따뜻하다' → ?"
AI:   "긍정"   (= 양식 정확히 따름)
```

### 추출 작업

```text
[Zero-shot]
USER: "이 이메일에서 회사명·발신자·요청을 뽑아줘"
AI:   "회사: ABC, 발신자: 홍길동, 요청: 미팅 잡기..."
       (= 형식이 매번 다름)

[Few-shot — JSON 양식 강제]
USER: "다음 이메일에서 정보 추출:
       예시:
       입력: '안녕하세요. ABC의 홍길동입니다. 다음 주 화요일 미팅 가능할까요?'
       출력: {\"company\": \"ABC\", \"sender\": \"홍길동\", \"request\": \"미팅\"}

       입력: '안녕하세요. XYZ의 김영희입니다. 견적서를 보내주실 수 있을까요?'
       출력: ?"
AI:   {\"company\": \"XYZ\", \"sender\": \"김영희\", \"request\": \"견적서\"}
       (= 항상 같은 형식)
```

## 라이브 시연 가능한 예시

```bash
[강의 화면 A — Zero-shot]
> "한국 동요 중 비슷한 거 3개 알려줘"
→ Claude: "1. 학교종 2. 곰 세 마리 3. 산토끼"  (선택이 자유로움)

[강의 화면 B — Few-shot]
> "동요 추천:
   '곰 세 마리' → 동물·가족 주제
   '학교종' → 학교 일상
   '산토끼' → ?"
→ Claude: "산토끼 → 동물·자연 주제"  (양식 박힘)
```

## 4. 실제 효과 (수치)

- **GPT-3 (2020)** 논문: Few-shot이 zero-shot 대비 *10~30%p* 정확도 상승 (분류 작업).
- **Claude 4 (2026)**: 모델이 똑똑해지면서 *zero-shot* 도 거의 few-shot 수준 — 그러나 *형식 일관성*에는 여전히 few-shot 필수.
- **2026 트렌드**: *프롬프트 길이 비용* 때문에 — 가능하면 zero-shot, 양식 일관성이 핵심일 때만 few-shot.

## 한계

- **예시가 편향**되면 모델도 편향: 부정적 예시만 3개 주면 모델이 부정 쪽으로 기움.
- **너무 많은 예시는 역효과**: 5개 넘어가면 [Lost in the Middle](../../phenomena/Lost-in-the-Middle.md) 위험. 3개가 sweet spot.
- **단순 추론 작업**에는 zero-shot CoT가 더 효과적 (예시보다 *단계 사고*).

## 꼬리에 꼬리 (관련 개념)

- [프롬프트 엔지니어링](../프롬프트-엔지니어링.md) — 부모 문서
- [Chain-of-Thought](chain-of-thought.md) — 추론 강화 — few-shot 과 결합 강력
- [Role Prompting](role-prompting.md) — 역할 부여
- [Self-Consistency](self-consistency.md) — 다중 샘플링 검증
- [Meta-Prompting](meta-prompting.md) — 메타·체이닝

## 출처

- [GPT-3 paper — Language Models are Few-Shot Learners (Brown et al., 2020)](https://arxiv.org/abs/2005.14165) — 원전
- [Codecademy: Zero-Shot, One-Shot, Few-Shot](https://www.codecademy.com/article/prompt-engineering-101-understanding-zero-shot-one-shot-and-few-shot) — 입문 비교
- [IBM: What is zero-shot prompting](https://www.ibm.com/think/topics/zero-shot-prompting) — Zero-shot 정의
- [Prompting Guide — Zero-Shot](https://www.promptingguide.ai/techniques/zeroshot) — 종합
