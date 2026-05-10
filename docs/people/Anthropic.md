# Anthropic

> Claude·Claude Code·MCP를 만든 회사. **2021년 창립**, 7명의 OpenAI 출신이 *"AI 안전"을 회사의 출발점*으로 삼아 만든 미국 샌프란시스코 본사 AI 연구·제품 회사. 강의 전반에서 인용되는 *"Anthropic이 만든 ~"* 의 그 회사다.

> 카테고리 노트: *회사*는 일반적으로 `companies/`에 들어가야 하지만, 현 시점 `companies/` 후보는 Anthropic 단독이라 — `docs/CLAUDE.md` §1 규칙(후보 1개면 새 폴더 안 만든다)에 따라 `people/`에 우선 배치. OpenAI·Google 등 추가 후보가 생기면 `companies/`로 이전.

## 1. 왜 "Anthropic"이라고 부르나

- **어원**: 그리스어 *anthropos(ἄνθρωπος, 인간)* 에서 온 형용사 *anthropic*. 우주론에서 *"인간 중심 원리(anthropic principle)"* 라는 표현이 유명. 즉 — *AI를 인간 중심으로* 만들겠다는 회사 철학을 이름에 박아넣음.
- **창립**: **2021년**, 미국 샌프란시스코.
- **창립 멤버 7명** — 모두 OpenAI 출신:
  - **Dario Amodei** (CEO) — OpenAI VP of Research. GPT-2·GPT-3 시기 모델 개발 총괄.
  - **Daniela Amodei** (President, Dario의 누이) — OpenAI VP of Safety & Policy. 2020년 OpenAI 떠남.
  - **Jared Kaplan** (Chief Science Officer) — 스케일링 법칙 논문 1저자.
  - **Sam McCandlish** (Chief Architect)
  - **Tom Brown** — GPT-3 논문 1저자.
  - **Jack Clark** — OpenAI 정책팀 출신, Anthropic 정책 책임.
  - **Christopher Olah** — 해석가능성(interpretability) 연구 리드.
  - **Benjamin Mann** — Anthropic Labs 책임.
- **법인 형태**: *Public Benefit Corporation (PBC, 공익 법인)*. 이사회가 주주 이익뿐 아니라 *"AI가 인류와 사회의 번영에 기여하도록"* 이라는 사명 추구도 *법적으로* 우선시할 수 있는 구조. 일반 영리 회사와 다른 점.

## 2. 그전에는 어떤 문제가 있었나

2020년 시점 AI 업계의 풍경:

- **AI safety vs 제품 출시 속도** 사이의 긴장 — 안전 검토를 강하게 걸면 제품이 늦어지고, 빨리 내보내면 안전 절차가 묽어진다.
- **OpenAI 내부 갈등** — 안전팀과 제품팀의 우선순위가 자주 충돌. 2020년 GPT-3 출시·제품화 가속 시기에 Amodei 남매를 비롯한 안전팀 핵심 인력들이 *방향성 차이*로 떠난다.
- ***안전 우선* 을 회사 철학의 출발점으로 박아둔 회사가 없었다** — 안전팀이 회사 안에서 *부서 하나*로 존재하는 모델은 결국 우선순위 싸움에서 밀린다는 학습.

**일상 비유**: *제약회사를 차릴 때, 부작용 검증부서를 *나중에* 만들 것인가, *처음부터* 만들 것인가*. 후자를 선택한 사람들이 OpenAI에서 나와 만든 회사가 Anthropic이다.

## 3. 어떻게 해결했나 — 회사 자체를 *안전 기반*으로 설계

### (1) Constitutional AI (CAI) — RLHF에서 RLAIF로

OpenAI가 정착시킨 *RLHF(인간 피드백으로 강화학습)* 의 한계 — *사람 검토자의 수가 모델 출력의 양을 따라가지 못한다*. Anthropic은 *AI가 *원칙 문서(constitution)*를 보고 자기 출력을 평가·교정* 하게 만드는 *RLAIF* 방식을 정착시켰다. 2022년 발표.

### (2) 주요 제품 라인업 (2026-05 기준)

| 제품 | 출시 | 한 줄 |
|---|---|---|
| **Claude API** | 2023 | 개발자용 API |
| **Claude.ai** | 2023 | 일반 사용자용 채팅 (ChatGPT 대응) |
| **MCP (Model Context Protocol)** | 2024-11 공개 / 2025-12 Linux Foundation 기증 | AI ↔ 외부 도구 연결 표준 |
| **Claude Code** | 2025-02 정식 출시 | 공식 CLI 코딩 도구 |
| **Claude 4 / 4.5 / 4.6 / 4.7 라인업** | 2025~2026 | Opus·Sonnet·Haiku 3등급 모델 |

→ 2024-11 *MCP* 공개와 2025-02 *Claude Code* 출시가 *바이브코딩 흐름*의 두 큰 분기점이었다.

### (3) 자금·시장 위치

- 주요 투자자: **Google**, **Amazon**, **Spark Capital** 등 다단계 라운드.
- 2026-05 기준, OpenAI와 함께 *최상위 LLM 모델 제공자* 양강. SWE-bench·MMLU 등 주요 벤치마크에서 Claude 4 Opus·Sonnet 라인이 OpenAI GPT-5와 1·2위를 다투는 위치.
- *기업·개발자 시장*에서 특히 강하다 (안전성·코딩 능력으로 평가받음). 일반 소비자 시장은 ChatGPT가 우위.

## 4. 강의에서 *왜* 이 회사를 알아야 하나

이 강의 전체에서 사용하는 도구·프로토콜 *대부분*이 Anthropic 산.

- **Claude Code 도입부** — *"Claude Code는 **Anthropic이라는 회사**가 만든 공식 CLI 도구"*
- **MCP 도입부** — *"**Anthropic**이 2024년에 공개한 표준(MCP)"*
- **시스템 프롬프트 섹션** — Claude Code 시스템 프롬프트 유출 사건 (Anthropic 내부 시스템 설계 일부 공개)
- **하니스 정의 섹션** — *Anthropic의 정의*: *"하니스 = 모델이 아닌 나머지 전부"* 가 강의 핵심 명제

청중에게 줄 1줄 메시지: *"강의에서 쓰는 도구의 다수가 같은 회사 — Anthropic — 에서 나옵니다. AI 안전을 출발점으로 삼은 회사라는 사실이, *왜 Claude Code 안에 권한 시스템·시스템 프롬프트 같은 안전장치가 깊게 박혀있는지* 를 설명해줍니다."*

## 5. 라이브 시연 가능한 예시

청중이 즉시 직접 확인 가능한 *Anthropic의 공개 자세*:

- `https://www.anthropic.com/research` — 연구 논문을 공개. 회사 *블로그처럼* 읽을 수 있음.
- `https://www.anthropic.com/transparency` — 자사 모델의 *위험 평가 보고서* 공개.
- `https://github.com/anthropics/anthropic-cookbook` — 사용 예시·패턴을 오픈소스로 공유.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code](../tools/Claude-Code.md) — Anthropic 공식 CLI
- [CLAUDE.md](../tools/CLAUDE-md.md) — Anthropic이 정한 프로젝트 메모리 표준
- [MCP](../tools/MCP.md) — Anthropic이 2024년 공개한 외부 도구 연결 프로토콜
- [Claude Code 시스템 프롬프트](../tools/Claude-Code-시스템프롬프트.md) — Anthropic이 *어떻게 안전을 텍스트로 박아두었나* 사례
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — *"하니스 = 모델이 아닌 나머지 전부"* 정의 출처
- [Andrej Karpathy](Andrej-Karpathy.md) — *"바이브코딩"* 용어 정착 인물 (Anthropic 소속 아님 — OpenAI 공동창립자, 2024 Tesla AI/Eureka Labs 행보)
- [LLM](../concepts/LLM.md) — Claude도 LLM의 한 사례
- [oh-my-claudecode](../tools/oh-my-claudecode.md) — Anthropic이 만들지 않은, 커뮤니티의 Claude Code 확장 사례

## 출처

- [Anthropic — Wikipedia](https://en.wikipedia.org/wiki/Anthropic) — 창립·연혁·제품·자금
- [Dario Amodei — Wikipedia](https://en.wikipedia.org/wiki/Dario_Amodei) — CEO 약력
- [Daniela Amodei — Wikipedia](https://en.wikipedia.org/wiki/Daniela_Amodei) — President 약력
- [Anthropic 공식 사이트](https://www.anthropic.com/) — 연구·제품·정책
- [Britannica — Who founded Anthropic](https://www.britannica.com/question/Who-founded-Anthropic-the-makers-of-Claude-AI-and-why) — 창립 배경 요약
- [TIME 100 AI 2023 — Dario and Daniela Amodei](https://time.com/collection/time100-ai/6309047/daniela-and-dario-amodei/) — 인물 소개
