# RAG (Retrieval-Augmented Generation, 검색 증강 생성)

> AI에게 답하기 전에 **신뢰 가능한 문서를 먼저 검색해서 함께 보여주는** 기법. 환각을 줄이는 가장 강력한 수단 중 하나.

## 1. 왜 "RAG"라고 부르나

- **Retrieval (검색)**: 답하기 전, 외부 데이터베이스나 문서에서 **관련 정보를 끌어온다**
- **Augmented (증강된)**: 모델의 본래 지식에 검색 결과를 **얹어 보강**한다
- **Generation (생성)**: 그 위에서 답을 **만든다**
- 세 단계의 머리글자 = **R-A-G**
- **누가·언제**: **2020년 5월 22일**, Meta AI(당시 Facebook AI Research)의 **Patrick Lewis** 외 공저자들이 arXiv에 논문 공개. NeurIPS 2020에서 정식 발표.
- **재밌는 비하인드**: Lewis 본인은 "RAG"라는 약어가 별로라며 "더 좋은 약자였으면 좋았을 것"이라고 농담 — 영어 "rag"는 "넝마"라는 뜻도 있다. 그러나 지금은 수백 개 논문, 수십 개 상용 서비스가 쓰는 표준 용어.

## 2. 그전에는 어떤 문제가 있었나

- LLM은 학습 시점까지의 데이터만 안다 (예: GPT-4 학습 컷오프 = 2023년)
- 학습 이후에 일어난 일, 회사 내부 문서, 사용자 개인 자료 등은 **모른다**
- 모르는 걸 모른다고 답하면 좋겠지만, LLM은 **그럴듯한 거짓말(환각)** 을 만들어낸다
- 모델 자체에 더 많은 지식을 넣으려면 **재학습**이 필요한데, 비용이 크고 자주 못 한다

**일상 비유**: 신입 변호사에게 어제 판결문 내용을 묻는 격. 학교에서 배운 판례만으로 추측해서 답하면 틀린다. 그러나 옆에 **오늘 자 판례 데이터베이스**를 두고 검색해서 보면서 답하게 하면 훨씬 정확하다. RAG가 그 데이터베이스다.

## 3. 어떻게 해결했나

RAG의 동작 흐름:

1. **사용자 질문 입력**: "회사 휴가 정책은?"
2. **검색 (Retrieval)**: 회사 위키/HR 문서에서 관련 페이지를 자동으로 찾는다 (보통 벡터 검색 = 의미 기반 검색)
3. **컨텍스트 주입**: 찾은 문서 내용을 LLM 프롬프트에 함께 넣는다
4. **생성 (Generation)**: LLM이 그 문서를 보면서 답을 만든다
5. (선택) **출처 표기**: 어느 문서에서 가져왔는지 답변에 함께 표시 → 사용자 검증 가능

**효과**:
- 환각 현저히 감소 (답의 근거가 컨텍스트에 있으므로)
- 모델 재학습 없이 **최신 정보** 반영 가능
- 회사 내부 문서, 개인 자료 등 **비공개 데이터** 활용 가능
- 출처 표기로 **신뢰성** 확보

**1강 연결 포인트**:
- "환각" 섹션에서 "그래서 우리가 그냥 던지면 안 되는 거죠" 메시지의 실무적 답
- 컨텍스트 엔지니어링의 대표적 구현 사례

## 한계

- 검색 품질이 나쁘면 GIGO (쓰레기 들어가면 쓰레기 나옴) — 관련 없는 문서를 끌어오면 답도 틀린다
- 검색·임베딩 인프라가 별도로 필요
- 컨텍스트 창에 들어갈 수 있는 양에 한계 — 어떤 문서를 우선 넣을지 설계가 중요

## 꼬리에 꼬리 (관련 개념)

- [컨텍스트 엔지니어링](컨텍스트-엔지니어링.md) — RAG의 상위 개념
- [환각](../phenomena/환각.md) — RAG가 푸는 핵심 문제
- [LLM](../concepts/LLM.md) — RAG의 G(Generation) 담당
- **Vector Database / Embedding** — RAG의 검색 단계 핵심 기술 (필요 시 별도 문서)

## 출처

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020) — arXiv:2005.11401](https://arxiv.org/abs/2005.11401) — 원논문
- [Retrieval-Augmented Generation — Meta AI Research](https://ai.meta.com/research/publications/retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks/) — Meta 공식 페이지
- [What Is Retrieval-Augmented Generation, aka RAG (NVIDIA Blogs)](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) — Patrick Lewis 인터뷰 포함, 비전공자용 입문
