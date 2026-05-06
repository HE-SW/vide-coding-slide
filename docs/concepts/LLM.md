# LLM (Large Language Model, 대규모 언어 모델)

> 엄청난 양의 텍스트를 학습해서 **다음에 올 단어를 예측**하는 초거대 AI. 한 줄이면 충분하다.

## 1. 왜 "Large Language Model"이라고 부르나

- **Language Model (언어 모델)**: NLP에서 오래된 개념. "이 단어 다음에 어떤 단어가 올 확률이 가장 높은가"를 계산하는 통계 모델. 1990년대~2010년대 초반에는 n-gram 기반 모델이 주류였다.
- **Large**: 2017년 Transformer 등장 이후 모델의 **파라미터 수**(가중치 개수)와 **학습 데이터 양**이 폭증했다. 기존 언어 모델 대비 수천~수만 배 규모가 되면서 그냥 "language model"이 아니라 **large** language model로 구분해 부르게 됐다.
- **언제 용어가 정착됐나**: 2018년 Google BERT, OpenAI GPT-1 출시 이후 점진적으로 사용되기 시작했고, 2020년 GPT-3 (1,750억 파라미터)를 계기로 학계와 업계 모두에서 표준 용어로 굳어졌다.
- **누가 콕 집어 만든 단어는 아니다** — 특정 인물이 발명한 신조어가 아니라, 모델 규모가 커지면서 자연스럽게 자리 잡은 기술 용어.

## 2. 그전에는 어떤 문제가 있었나

- **n-gram 모델**: 직전 N개 단어만 보고 다음을 예측. "오늘 날씨가" 다음에 "맑다/흐리다"는 맞히지만, **긴 문맥**을 기억하지 못했다.
- **RNN/LSTM (2010년대)**: 긴 문맥을 어느 정도 다뤘지만, 학습이 느리고 병렬화가 어려웠다. 문장이 길어질수록 앞쪽 정보를 잊어버리는 "장기 의존성" 문제도 컸다.
- **결과**: 챗봇은 어색한 답변을 하고, 번역기는 문맥을 놓치고, 글 요약은 핵심을 빗나갔다. 사람과 대화하는 듯한 자연스러움은 먼 이야기였다.

**일상 비유**: 옛날 휴대폰 자동 완성 키보드를 떠올려보자. 직전 한두 단어만 보고 추천하니까 문장 전체 흐름과 어긋나는 추천이 자주 나왔다. LLM 이전 언어 모델은 그 수준에 가까웠다.

## 3. 어떻게 해결했나

- **2017년 "Attention Is All You Need"** (Vaswani et al., Google) — Transformer 아키텍처 발표. **Attention** 메커니즘으로 문장 내 모든 단어를 동시에 참고할 수 있게 되어, 긴 문맥과 병렬 처리가 동시에 가능해졌다.
- **2018년**: 같은 해 BERT(Google)와 GPT-1(OpenAI)가 Transformer 기반으로 출시. 사전 학습(pre-training) + 파인튜닝 패러다임 정착.
- **2020년 GPT-3**: 175B 파라미터로 "그냥 크게 만들기만 해도 새로운 능력이 창발한다(emergent ability)"는 점이 드러나면서 LLM 시대 본격 개막.
- **2022년 ChatGPT** 출시 후 일반 대중에게 LLM이 알려졌고, **2025년 현재** Claude·Gemini·GPT-4/5 등 다양한 LLM이 일상 도구가 되었다.

**1강 연결 포인트**: 바이브코딩이 가능해진 결정적 기술 토대. "자연어 → 코드" 변환의 게임 체인저.

## 꼬리에 꼬리 (관련 개념)

- **Transformer / Attention** — LLM의 기반 아키텍처. (필요 시 별도 문서 추가)
- **GPT, BERT** — 최초의 Transformer 기반 LLM 계열. (필요 시 별도 문서 추가)
- [환각](../phenomena/환각.md) — LLM의 가장 큰 한계
- [바이브코딩](바이브코딩.md) — LLM 성능 향상이 만든 새 코딩 방식

## 출처

- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) — Transformer 원논문
- [Large language model — Wikipedia](https://en.wikipedia.org/wiki/Large_language_model) — 용어 정의와 역사
- [A Brief History of LLMs (Medium, LM Po)](https://medium.com/@lmpo/a-brief-history-of-lmms-from-transformers-2017-to-deepseek-r1-2025-dae75dd3f59a) — 2017~2025 타임라인
- [What is a Transformer Model? (IBM)](https://www.ibm.com/think/topics/transformer-model) — 비전공자용 입문 설명
