# Tokenization (토큰화)

> LLM이 글자를 **단어 덩어리(토큰)** 로 잘라 보는 방식. **"strawberry에 R이 몇 개?"** 같은 단순한 질문을 LLM이 자주 틀리는 이유.

## 1. 왜 "Tokenization"이라고 부르나

- **Token(토큰)**: 영어로 "표시·증표·기호". 컴퓨터과학에서 **의미를 가진 최소 단위**를 가리키는 오래된 용어 (예: 컴파일러가 코드를 토큰 단위로 쪼갬).
- **-ize**: "~로 만들다"라는 동사화 접미사.
- 합치면 **"의미 단위로 쪼개는 작업"**.
- **NLP 분야 도입**: 1990년대 이전부터 자연어 처리 전반에서 사용.
- **LLM 시대 표준 = BPE (Byte-Pair Encoding)**: 1994년 데이터 압축용으로 발명된 알고리즘이 **2016년 Sennrich 외**가 신경망 기계번역에 적용하면서 NLP 표준이 됨. GPT 시리즈, Claude, LLaMA 모두 BPE 또는 변형(SentencePiece, tiktoken 등) 사용.

## 2. 그전에는 어떤 문제가 있었나

LLM 이전엔 두 극단이 있었다:

| 방식 | 장점 | 단점 |
|---|---|---|
| **글자 단위(character)** | 어떤 단어든 처리 | 시퀀스가 너무 길어서 학습이 느림 |
| **단어 단위(word)** | 빠르지만 | 신조어·오타·외국어 단어를 모름 (vocabulary out of range) |

→ 둘 다 비효율. **타협점**이 필요했다.

## 3. BPE가 어떻게 해결했나

**BPE의 아이디어**: 자주 함께 등장하는 글자 쌍을 점점 합쳐서 **자주 쓰는 덩어리는 한 토큰, 드문 단어는 여러 토큰**으로.

예시 (실제 GPT 토큰):
- `the` → 1개 토큰 (자주 등장)
- `strawberry` → **`straw` + `berry`** 2개 토큰
- `antidisestablishmentarianism` → 6~7개 토큰

**효과**:
- 어휘 크기를 5만~10만 수준으로 유지하면서
- 새 단어도 조각조각 처리 가능
- 학습/추론 속도 모두 빨라짐

## "Strawberry에 R이 몇 개?" 문제

비개발자 강의에서 **가장 강력한 데모**.

**왜 LLM이 자주 "2개"라고 틀리는가**:

1. 모델이 보는 건 글자 `s-t-r-a-w-b-e-r-r-y`가 아니라 토큰 `[straw][berry]`
2. 각 토큰은 **하나의 벡터**(숫자 묶음)로 변환되어 그 안의 글자 정보가 **녹아 사라짐**
3. 모델은 "straw에 r이 1개, berry에 r이 2개"를 명시적으로 학습하지 않음
4. 학습 목표가 **다음 토큰 예측**이지 글자 세기가 아니라서, 글자 단위 attention이 약함

**일상 비유**: "딸기"라는 단어를 보면 우리는 글자 ㄸ-ㅏ-ㄹ-ㄱ-ㅣ를 자동으로 인식한다. 그러나 LLM은 "딸기"를 **하나의 그림 카드**로 본다. 카드 안에 어떤 자음·모음이 있는지 일일이 보지 않는다.

**우회 방법** (실제로 잘 됨):
- "**한 글자씩 나눠서** 세어줘"라고 명시 → 모델이 글자 단위로 처리
- "**s t r a w b e r r y**"처럼 공백을 넣어 입력 → 토크나이저가 글자 단위로 자름
- "단계별로 추론해줘 (Chain-of-Thought)" → 모델이 천천히 계산

→ 같은 모델이 같은 질문에 대해 **프롬프트만 바꾸면** 정답을 맞히는 라이브 시연이 가능.

## 강의 연결 포인트

- *"AI가 똑똑하다면서 R 개수도 못 세요?"* 라는 청중의 직관과 정면충돌하는 흥미 포인트.
- **"AI는 글자가 아니라 토큰을 본다"** 한 줄로 정체를 풀어주면, 청중이 "AI의 한계는 어디에서 오는가"를 처음으로 이해.
- 강의 핵심 메시지 **"좋은 결과는 우연이 아니라 설계"** 의 가장 직관적 근거 — 같은 모델이라도 **프롬프트 설계**에 따라 정답률이 달라진다.

## 꼬리에 꼬리 (관련 개념)

- [LLM](LLM.md) — 토큰화의 적용 주체
- [Transformer](Transformer.md) — 토큰을 처리하는 아키텍처
- [환각](../phenomena/환각.md) — 토큰화 한계가 환각의 한 원인
- [프롬프트 엔지니어링](../techniques/프롬프트-엔지니어링.md) — 토큰화 우회 기법의 무대

## 출처

- [Why LLMs Can't Count the R's in 'Strawberry' (Arbisoft)](https://arbisoft.com/blogs/why-ll-ms-can-t-count-the-r-s-in-strawberry-and-what-it-teaches-us) — 비전공자용 입문
- [The "Strawberry R Counting" Problem in LLMs (secwest.net)](https://www.secwest.net/strawberry) — 원인과 해결책 정리
- [Counting Ability of LLMs and Impact of Tokenization (arXiv:2410.19730)](https://arxiv.org/html/2410.19730v2) — 학술 분석
- [BPE vs Byte-level Tokenization: Why LLMs Struggle with Counting (SOTAAZ)](https://blog.sotaaz.com/post/bpe-vs-byte-level-tokenization) — BPE 메커니즘 해설
- [LLM breakdown 1/6: Tokenization (Mike Cohen)](https://mikexcohen.substack.com/p/llm-breakdown-16-tokenization-words) — 시각화 포함 입문
