# Lost in the Middle (가운데에서 길을 잃다)

> 긴 컨텍스트를 줘도 LLM은 **시작과 끝만 잘 보고 가운데는 무시**한다. *"GPT/Claude/Gemini가 점점 멍청해진다"의 두 번째 메커니즘.*

## 1. 왜 "Lost in the Middle"이라고 부르나

- 영어 표현 그대로 **"가운데에서 길을 잃다"**. 컨텍스트의 양 끝은 잘 활용되는데 중간 정보는 모델이 놓치는 모습을 직관적으로 묘사.
- **누가·언제**: **2023년 7월 6일**, **Nelson F. Liu** (Stanford) 외 6명(Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, **Percy Liang**) 이 arXiv에 논문 *"Lost in the Middle: How Language Models Use Long Contexts"* (arXiv:2307.03172) 공개. **TACL 2024**에 정식 게재.
- **왜 이 이름**: 결과가 너무 직관적이라 다른 이름을 고민할 필요가 없었다. **U자 모양 성능 곡선**이 핵심 증거 — 입력 처음·끝에서 정확도가 높고, 가운데에서 뚝 떨어진다.

## 2. 그전에는 어떤 문제가 있었나

2023년 들어 LLM 컨텍스트 창이 폭발적으로 길어졌다:
- GPT-3.5: 4K 토큰
- GPT-4: 8K → 32K → 128K
- Claude 2: 100K → 200K
- 현재 (2026): Claude Opus 4.7 1M, Gemini 2M

업계의 가정: *"창이 길어지면 모델이 더 많은 정보를 활용해 답을 잘 만들 것이다."*

그런데 사용자들이 체감하는 건 정반대였다:
- 긴 문서를 통째로 넣으면 답 품질이 **오히려 떨어진다**
- 대화가 길어지면 모델이 **앞에 한 약속을 지키지 않는다**
- "방금 한 말 무시해주세요"가 무시되지 않는다

이 직관을 **수치로 증명**한 게 Liu et al. 2023.

## 3. 무엇을 발견했나

논문의 핵심 실험:
- 다중 문서 질의응답: 정답이 들어 있는 문서를 컨텍스트의 **시작 / 가운데 / 끝**에 위치시킴
- 키-값 검색: 1,000개 키-값 쌍 중 하나를 묻고, 정답이 들어 있는 위치를 바꿈

**결과**:
- 정답이 **컨텍스트 시작**에 있을 때 정확도 최고
- **끝**에 있을 때도 비교적 높음
- **가운데**에 있을 때 정확도 **20~30%까지 폭락**
- 컨텍스트가 길수록 가운데 효과가 더 심해짐

→ **U자 모양 성능 곡선** (정확도 vs 정답 위치)

## 왜 이런 일이 일어나나 (간단히)

- Transformer의 어텐션 메커니즘은 모든 위치를 동등하게 다룬다고 알려졌지만, 실제 학습된 모델은 **위치 편향(position bias)** 을 보인다
- 학습 데이터에서 중요한 정보는 보통 **문서 시작·끝에 배치**되는 경향 → 모델이 그 패턴을 학습
- 긴 컨텍스트 학습이 부족하면 가운데 토큰을 충분히 활용하는 법을 배우지 못함

## 어떻게 대응하나 (1강 실무 메시지)

- **중요한 지시는 시스템 프롬프트(맨 앞) + 사용자 메시지(맨 뒤)에 둘 다 넣기**
- **컨텍스트가 길어지면 핵심을 다시 요약해서 끝에 한 번 더 붙이기**
- 새 세션을 자주 시작 (대화가 비대해지기 전에)
- RAG로 정말 필요한 자료만 추려 넣기 (양이 줄면 가운데 문제도 줄어든다)
- 2024년 이후 모델들은 학습 단계에서 가운데 활용 훈련을 강화 → 신모델일수록 완화 추세, 그러나 **완전 해소되지 않음**

## 1강 강의 연결 포인트

- *"GPT/Claude/Gemini를 쓰다 보면 점점 멍청해진다"* 의 **두 메커니즘** 중 두 번째 (첫 번째는 컨텍스트 창 자체의 한계로 잘려나가는 것):
  1. **Cutoff**: 창에서 잘려 사라진다
  2. **Lost in the Middle**: 안 잘려도 가운데를 모델이 무시한다
- 1강 메시지 *"좋은 결과는 우연이 아니라 설계"* 의 가장 구체적 근거 — **위치까지 의도적으로 설계**해야 한다.
- 컨텍스트 엔지니어링이 단순히 "자료를 많이 넣기"가 아니라 **순서와 위치까지 다루는 일**임을 보여주는 결정적 증거.

## 꼬리에 꼬리 (관련 개념)

- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — 위치 설계가 그 안의 핵심
- [LLM](../concepts/LLM.md) — 현상 발생 주체
- [Transformer](../concepts/Transformer.md) — 어텐션 위치 편향의 무대
- [Knowledge Cutoff](Knowledge-Cutoff.md) — "멍청해지는" 첫 번째 메커니즘과 짝

## 출처

- [Lost in the Middle: How Language Models Use Long Contexts (Liu et al., 2023, arXiv:2307.03172)](https://arxiv.org/abs/2307.03172) — 원논문
- [TACL 2024 게재본 (MIT Press)](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long) — 정식 출판본
- [Code & data on GitHub (nelson-liu)](https://github.com/nelson-liu/lost-in-the-middle) — 재현 가능한 실험 코드
- [Stanford CS PDF](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf) — 1저자 호스팅 PDF
