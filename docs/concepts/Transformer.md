# Transformer

> **모든 LLM의 뼈대가 된 신경망 구조.** 2017년 Google이 발표. "이 단어는 문장 안 다른 어떤 단어를 주목해야 하는가"를 모델 스스로 학습하게 만든 발명.

## 1. 왜 "Transformer"라고 부르나

- **Transform(변환하다)**: 입력 시퀀스를 출력 시퀀스로 **변환**한다는 뜻. 원래 기계 번역(영어 → 독일어처럼 한 시퀀스를 다른 시퀀스로 바꾸는 작업)을 풀기 위해 설계됐기에 자연스럽게 이 이름이 붙었다.
- **Transformers (영화/완구)**와는 무관. 그저 영어 동사 transform에서 온 기술 명칭.
- **언제·누가**: 2017년 6월 12일, **Ashish Vaswani 등 Google Brain/Google Research 소속 8명**이 arXiv에 논문 공개. 12월 NeurIPS에서 정식 발표.
- **논문 제목**: ***"Attention Is All You Need"*** — 제목 자체가 선언적이다. "이전에 쓰던 RNN·CNN 구조 다 빼고, **어텐션만 있으면 충분하다**"는 도발적 메시지.

## 2. 그전에는 어떤 문제가 있었나

- **RNN (Recurrent Neural Network) / LSTM**: 2010년대 NLP의 주류 구조. 단어를 **하나씩 순서대로** 처리.
  - 단어가 50개라면 50번을 순차적으로 계산해야 함 → **느리다**
  - 문장이 길어지면 앞쪽 정보를 잊는다 → **장기 의존성 문제**
  - 병렬 처리가 안 되니 GPU를 제대로 못 쓴다 → **학습이 느리다**
- **CNN (Convolutional Neural Network)**: 병렬 처리는 되지만 긴 문맥을 잡기 어려웠다.

**일상 비유**: 책을 읽을 때 첫 페이지부터 한 자씩 차례로 읽으면 마지막 장에 도달할 즈음 첫 장 내용을 잊어버린다. RNN/LSTM이 그랬다.

## 3. 어떻게 해결했나

**Attention(어텐션) 메커니즘**으로 단번에 풀었다:

- 문장 안 모든 단어가 **다른 모든 단어를 동시에 참고**할 수 있다 (Self-Attention)
- 어떤 단어를 얼마나 참고할지 **모델 스스로 학습**
- 순서대로 처리할 필요가 없으니 **완전 병렬화** → GPU 효율 극대화
- 결과: 동일한 학습 시간에 훨씬 큰 모델을 만들 수 있게 됐고, **모델이 커질수록 성능이 향상**되는 길이 열렸다

**역사적 영향**:
- 2018년 BERT (Google), GPT-1 (OpenAI) — Transformer 기반 첫 LLM
- 2020년 GPT-3, 2022년 ChatGPT — 모두 Transformer 변형
- "이름도 GPT(Generative **Pre-trained Transformer**)에 들어 있다"는 점이 단서
- 논문 발표 후 8명 저자 전원이 Google을 떠나 다른 회사에 합류하거나 창업 — AI 산업 전체에 흩어져 영향력 확산

## 일상 비유 — 어텐션을 한 줄로

**회의실에서 한 사람이 발언할 때, 청중은 *모든 사람의 표정을 동시에* 본다**. 누구의 표정이 가장 *정보가 많은지*에 따라 *주목하는 정도*가 달라진다. 이게 셀프 어텐션.

또 다른 비유: 영화를 볼 때 *주인공의 한 마디*가 던져지면 — 우리 머릿속에서 *그 영화의 다른 장면들*이 동시에 떠올라 의미가 합쳐진다. 한 단어를 처리할 때 *문장 안의 모든 단어*를 동시에 참고하는 어텐션과 동일한 행동.

## Before / After — RNN vs Transformer

```text
[BEFORE — RNN/LSTM (2010년대)]
"오늘   날씨가   정말   [____]"
 →      →       →       →    한 단어씩 순차 처리
                            앞 단어를 잊을 위험

[AFTER — Transformer (2017~)]
"오늘   날씨가   정말   [____]"
 ↕      ↕       ↕       ↕   모든 단어가 동시에 서로를 참조
 ↕━━━━━↕━━━━━━↕━━━━━↕   GPU에서 완전 병렬 가능
```

## 라이브 시연 가능한 예시

직접 어텐션을 시각화하는 게 어려우므로 *말로* 시연:

```text
[강의 중에 칠판/슬라이드에]
문장: "그 사람이 들어왔을 때 그녀는 웃었다."

질문: "그녀"는 누구인가?
RNN: 앞 단어들을 거치며 흐릿해짐 → 자주 틀림
Transformer: "그녀"가 *문장 전체*를 동시에 본다 →
            "그 사람"과의 관계를 파악 → 정확
```

## 실제 사례 (2017-2026 영향)

- **8명 저자의 흩어짐**: Vaswani(Essential AI), Shazeer(Character.AI → Google 복귀), Parmar(Adept), Uszkoreit(Inceptive), Jones(Cohere co-founder)·Gomez(Cohere CEO), Kaiser(OpenAI), Polosukhin(NEAR Protocol). **AI 산업 지도가 이 8명에서 시작된다는 농담이 있을 정도**.
- **2026년 현재**: 거의 모든 상용 LLM이 Transformer 기반. 변형은 다양 (Mixture-of-Experts, State Space Models 등 일부 도전자가 등장하지만 주류 안 됨).

## 꼬리에 꼬리 (관련 개념)

- [LLM](LLM.md) — Transformer 위에 만들어진 모든 거대 모델
- **Attention 메커니즘** — Transformer의 핵심 부품 (필요 시 별도 문서)
- **GPT, BERT** — Transformer로 만든 첫 세대 모델 (필요 시 별도 문서)

## 출처

- [Attention Is All You Need (arXiv:1706.03762)](https://arxiv.org/abs/1706.03762) — 원논문
- [Attention Is All You Need — Wikipedia](https://en.wikipedia.org/wiki/Attention_Is_All_You_Need) — 8명 저자, 출판 이력, 영향
- [Transformer (machine learning model) — Wikipedia](https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)) — 구조 해설
- [What is a Transformer Model? (IBM)](https://www.ibm.com/think/topics/transformer-model) — 비전공자용 입문
