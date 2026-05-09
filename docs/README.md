# 바이브코딩 강의 지식 베이스

비개발자 대상 4강짜리 바이브코딩 강의용 레퍼런스 문서 모음. 강의자가 청중에게 정확한 출처와 함께 개념을 전달할 수 있도록, 모든 문서는 다음 3-조건 서사를 따른다.

1. **왜 이렇게 부르나** — 이름의 유래 (인물·연도·어원)
2. **그전에는 어떤 문제가 있었나** — 등장 직전의 한계
3. **어떻게 해결했나** — 이 개념이 가져온 변화

---

## 카테고리

### `concepts/` — 큰 개념
사람이 만든 패러다임/모델 종류. 한 시대를 가르는 분기점이 되는 단어들.

- [바이브코딩 (Vibe Coding)](concepts/바이브코딩.md) — 2025년 2월, 코드가 아니라 분위기로 만드는 새 흐름
- [LLM (Large Language Model)](concepts/LLM.md) — 다음 단어를 예측하는 초거대 AI
- [Transformer](concepts/Transformer.md) — 모든 LLM의 뼈대가 된 2017년 신경망 구조
- [Tokenization (토큰화)](concepts/Tokenization.md) — LLM이 글자를 단어 덩어리로 보는 방식. strawberry R 문제의 정체

### `techniques/` — 기법
실무에서 적용하는 방법론. "어떻게" 잘 쓰는가에 대한 답.

- [프롬프트 엔지니어링 (Prompt Engineering)](techniques/프롬프트-엔지니어링.md) — 무엇을 요청할 것인가
- [컨텍스트 엔지니어링 (Context Engineering)](techniques/컨텍스트-엔지니어링.md) — 어떤 정보를 함께 줄 것인가
- [하니스 엔지니어링 (Harness Engineering)](techniques/하니스-엔지니어링.md) — 어떻게 반복적으로 검증할 것인가
- [RAG (Retrieval-Augmented Generation)](techniques/RAG.md) — 검색해서 답하기, 환각의 가장 강력한 해독제

### `phenomena/` — 현상/한계
관찰되는 문제. 강의에서 "주의할 점"으로 짚어야 할 항목들.

- [환각 (Hallucination)](phenomena/환각.md) — LLM이 그럴듯하게 지어내는 거짓말
- [Sycophancy (아부)](phenomena/Sycophancy.md) — "이거 틀리지 않아?" 한 마디에 답을 뒤집는 현상
- [비결정성 (Non-Determinism)](phenomena/비결정성.md) — 같은 질문에 매번 다른 답이 나오는 이유
- [Knowledge Cutoff (지식 컷오프)](phenomena/Knowledge-Cutoff.md) — AI가 어제 일을 모르는 이유
- [Lost in the Middle](phenomena/Lost-in-the-Middle.md) — 컨텍스트 가운데를 LLM이 무시하는 위치 편향

### `people/` — 인물
강의에서 인용하거나 맥락 설명에 필요한 인물.

- [Andrej Karpathy](people/Andrej-Karpathy.md) — "바이브코딩"·"컨텍스트 엔지니어링" 두 용어를 정착시킨 인물

### `tools/` — 도구·제품
강의에서 시연하거나 청중이 실제로 써볼 도구의 사용 레퍼런스.

- [Claude Code](tools/Claude-Code.md) — Anthropic 공식 CLI. 슬래시 명령어 정리 (2026-05-07 기준)
- [왜 CLI인가](tools/CLI를-쓰는-이유.md) — claude.ai 채팅 vs Claude Code, 비개발자 청중을 위한 비교
- [CLAUDE.md](tools/CLAUDE-md.md) — Claude Code가 자동으로 읽는 프로젝트 메모리 파일
- [oh-my-claudecode (OMC)](tools/oh-my-claudecode.md) — Claude Code 위에 얹는 멀티 에이전트 오케스트레이션 플러그인 (32k★, MIT)
- [andrej-karpathy-skills](tools/andrej-karpathy-skills.md) — Karpathy의 LLM 4대 실패 패턴을 65줄 CLAUDE.md로 압축한 행동 가이드 (10만 ★, MIT)

### `rules/` — 프로젝트 행동 규율 (실제 적용 파일)
이 레포 자체에 적용하는 코딩 규율. 강의 시연 자료로도 사용된다.

- [coding-guidelines.md](rules/coding-guidelines.md) — Karpathy 4원칙(Think · Simple · Surgical · Goal-Driven)을 한국어 강의톤으로 옮긴 행동 가이드라인. 2강 *"한 장의 행동 규율을 어떻게 까는가"* 슬라이드 시연용.

### `methodologies/` — 개발 방법론
바이브코딩의 위치를 이해하기 위해 알아야 할 전·후 방법론.

- [워터폴 (Waterfall)](methodologies/워터폴.md) — 1970년 등장, 단계별 한 방향 흐름. 규율은 강하나 느림.
- [애자일 (Agile)](methodologies/애자일.md) — 2001년 선언. 속도는 얻었으나 문서·규율 손실.
- [하이퍼-워터폴 (Hyper-Waterfall)](methodologies/하이퍼-워터폴.md) — 2026년 edwardkim. AI 시대에 둘 다 가지려는 1인+AI 방법론.

---

## 사용 방법

- 강의 준비 시 `1강/script.md`의 각 섹션과 이 문서를 교차 확인
- 즉석 질문 대비: 각 문서 하단 **출처** 섹션에 1차/2차 자료 URL 정리
- 새 개념이 발견되면 적절한 카테고리에 추가 (필요 시 새 카테고리 신설)
