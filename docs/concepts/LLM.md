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
- **2022년 ChatGPT** 출시 후 일반 대중에게 LLM이 알려졌고, **2026년 현재** Claude (Opus 4.7 / Sonnet 4.6 / Haiku 4.5)·GPT-5.5·Gemini 3.1 등 다양한 LLM 라인업이 일상 도구로 자리 잡았다.

**1강 연결 포인트**: 바이브코딩이 가능해진 결정적 기술 토대. "자연어 → 코드" 변환의 게임 체인저.

## Before / After — LLM 발전 한눈에 보기

같은 작업이 시대마다 어떻게 달라졌는지:

| 작업 | 2018 (BERT) | 2020 (GPT-3) | 2022 (ChatGPT) | 2026 (Opus 4.7 / GPT-5.5) |
|---|---|---|---|---|
| **번역** | 단문은 OK, 문맥 약함 | 자연스러움 ↑ | 거의 사람 수준 | 사투리·문체까지 보존 |
| **코드 작성** | 자동완성 일부 | 짧은 함수 가능 | 한 페이지 코드 | 멀티파일 프로젝트 |
| **수학** | 거의 못 함 | 산수 정도 | 중학생 수준 | 올림피아드 수준 일부 |
| **추론** | 단문장 분류 | "왜?"에 답하기 시작 | Chain-of-Thought 유행 | 자체 추론 chain (o-series·Opus thinking) |

## 라이브 시연 가능한 예시

### 시연 — *"왜 LLM은 다음 단어를 예측한다고 하나"*
```bash
> "오늘 하늘이 정말 [______]"
→ Claude 답변 후보:
   "맑네요." (가능성 35%)
   "예쁘네요." (가능성 25%)
   "푸르네요." (가능성 15%)
   ...
   = LLM이 매 토큰마다 *확률 분포*를 계산하고
     그 중 하나를 *샘플링*하는 모습
```
청중에게 *"AI가 *생각*하는 게 아니라 *다음 단어를 확률로 고르는*다"*는 정체를 한 번에 와닿게 한다.

### 일상 비유 — *옛날 휴대폰 자동완성과 비교*
- T9 자판: 직전 한 단어만 보고 추천 → 답답함
- 스마트폰 키보드 (2010s): 직전 5~10개 단어 보고 문맥 파악 시도
- LLM (2020s~): 수만 토큰 보고 *논리·추론·문체*까지 일관되게 유지

같은 *"다음 단어 예측"*인데 — *얼마나 길게 보느냐*가 차원을 바꿨다.

## 실제 사건 (2024-2026 마일스톤)

- **2024-12 — OpenAI o1**: 추론 chain 자체를 학습한 첫 모델. *"빨리 답하기"*에서 *"오래 생각하고 답하기"*로 패러다임 이동.
- **2025 — Reasoning 시대 본격화**: Anthropic Claude 3.7 Sonnet의 *"extended thinking"*, Google Gemini 2.5 Deep Think 등 추론형 모델이 표준화.
- **2026-Q1 — 1M context window 보편화**: Claude Opus 4.7 1M 토큰, Gemini 3.1 Pro 2M 토큰. 책 한 권을 통째로 처리 가능.
- **2026 — 멀티모달 표준**: 텍스트뿐 아니라 이미지·오디오·코드 실행 결과까지 한 모델이 처리.

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
