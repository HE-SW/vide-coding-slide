# Knowledge Cutoff (지식 컷오프)

> LLM이 학습한 데이터의 **마지막 시점**. 그 이후에 일어난 일은 모델이 모른다. *"왜 우리가 지침과 자료를 함께 줘야 하는가"의 가장 직접적 이유.*

## 1. 왜 "Knowledge Cutoff"라고 부르나

- **Knowledge(지식)** + **Cutoff(끊는 시점)**. 직역하면 "지식이 잘린 날".
- 학술/업계 용어로 자연스럽게 자리 잡은 표현. 특정 인물이 만든 신조어가 아니라, OpenAI가 GPT-3·GPT-4 시스템 프롬프트에 *"My knowledge cutoff is..."* 형태로 명시하면서 표준이 됨.
- **Anthropic은 더 세분화** — Claude 공식 문서는 두 날짜를 구분:
  - **Reliable knowledge cutoff (신뢰 가능 컷오프)**: 모델이 정확히 답할 수 있는 시점
  - **Training data cutoff (학습 데이터 컷오프)**: 학습에 포함된 가장 최근 자료의 시점
  - 후자가 더 늦지만, 그 시점 자료는 양이 적어 모델 답이 부정확할 수 있음

## 2. 그전에는 어떤 문제가 있었나

LLM의 작동 방식 자체에서 따라 나오는 한계:

- LLM은 **학습 시점에 본 텍스트**의 패턴만 안다 — 검색 엔진처럼 실시간으로 인터넷을 찾는 게 아님
- 모델 학습은 수개월이 걸리고, 학습 후 안전성 검증·배포까지 **6~12개월** 추가 소요
- 결과: 사용자가 모델을 쓰는 시점에 모델은 **이미 6개월~1년 이상 과거**에 머물러 있음
- 사용자는 그걸 모르고 최신 정보를 묻는다 → 모델은 **모른다고 안 하고** 환각으로 답을 채운다

**일상 비유**: 작년에 구워낸 백과사전을 들고 다니는 천재 학생. 어제 뉴스를 물어보면 책에 없는데도 "음… 아마 이렇게 됐을 것"이라고 추측해서 답한다.

## 3. 어떻게 해결했나

근본적으로 "없앨" 수는 없다 (학습 비용 문제). 대신 **둘러서 해결**:

### (1) 모델 측 노력
- **모델 갱신 주기 단축** — 2022년엔 GPT-3.5가 2021년 9월 데이터로 1년 이상 사용됨. 2026년엔 분기 단위 업데이트가 표준.
- **시스템 프롬프트에 컷오프 명시** — 모델이 자기 한계를 인지하고 *"제 지식은 X월까지입니다"*라고 답하도록.

### (2) 사용자 측 우회 (1강 핵심)
- **컨텍스트 엔지니어링**: 최신 자료를 프롬프트에 직접 붙여 넣기
- **RAG (검색 증강 생성)**: 답하기 전에 자료를 자동 검색해 컨텍스트에 주입
- **웹 브라우징 도구**: 모델이 실시간 검색·페이지 읽기 가능 (ChatGPT Browse, Claude Web Search 등)
- **회사 내부 문서 RAG**: 학습된 적 없는 사내 위키·정책을 답할 수 있게 됨

## 주요 모델 컷오프 (2026-05-07 기준)

| 모델 | 컷오프 | 출처 |
|---|---|---|
| Claude Opus 4.7 | **2026년 1월** (Reliable & Training 동일) | Anthropic 공식 |
| Claude 4.6 Opus | 2025년 8월 | Anthropic 공식 |
| GPT-5.2 | 2025년 8월 | OpenAI |
| GPT-5.5 | 미공개 (2026년 4월 출시) | OpenAI |
| Gemini 3 | 2025년 1월 | Google |
| Gemini 3.1 Flash-Lite | 2025년 1월 | Google |

→ 각 모델 컷오프는 6개월 이내에 갱신되니, 강의 직전에 한 번씩 확인 권장.

## 1강 강의 연결 포인트

- *"AI는 모든 데이터를 학습하지 않았다. 최근 모델의 데이터는 항상 과거의 데이터다"* 메시지의 **정식 명칭**.
- "왜 우리가 지침과 자료를 함께 줘야 하는가"의 **가장 직접적이고 비기술적인 근거** — 모델은 어제 일을 모른다.
- **컨텍스트 엔지니어링**과 **RAG**가 등장한 이유로 자연스럽게 다리.
- 청중이 즉석에서 검증 가능: ChatGPT/Claude에게 *"오늘 날짜 알아?"* 또는 *"방금 출시된 X 알아?"*라고 물으면 한계를 직접 체험.

## 꼬리에 꼬리 (관련 개념)

- [LLM](../concepts/LLM.md) — 컷오프의 발생 주체
- [환각](환각.md) — 컷오프 이후 일을 모를 때 나오는 결과
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — 컷오프 우회의 기본기
- [RAG](../techniques/RAG.md) — 컷오프 우회의 표준 구현

## 출처

- [llm-knowledge-cutoff-dates (GitHub, HaoooWang)](https://github.com/HaoooWang/llm-knowledge-cutoff-dates) — 모델별 컷오프 종합 데이터베이스
- [AI Knowledge Cutoff Dates: Every Major LLM Updated (Temso AI, 2026)](https://www.temso.ai/blog/ai-knowledge-cutoff-dates-every-major-llm-updated-for-2026) — 2026년 갱신본
- [A comprehensive list of LLM knowledge cut off dates (ALLMO)](https://www.allmo.ai/articles/list-of-large-language-model-cut-off-dates) — 출처별 정리
