# MCP (Model Context Protocol)

> AI가 외부 서비스를 직접 다루게 해주는 **표준 통로**. GitHub 이슈를 직접 읽고, Figma 디자인을 가져오고, Google Drive 문서를 열어보는 식. **Anthropic이 2024년 11월 공개**, 2025년 OpenAI·Google 채택을 거쳐 2025-12 Linux Foundation 산하 *Agentic AI Foundation*에 기증.

## 1. 왜 "MCP"라고 부르나

- **Model Context Protocol**: *"모델에게 컨텍스트를 주는 표준 프로토콜"* 의 줄임말.
- **Anthropic**이 2024년 11월 발표 — *"AI 통합의 USB-C"* 라는 비유로 마케팅.
- 비유의 의미: USB-C가 *어떤 기기든 한 가지 모양으로 연결*되게 만든 것처럼, MCP는 *어떤 외부 서비스든 한 가지 형식으로 LLM과 연결*되게 만든다.
- 2025년 12월, Anthropic은 MCP를 **Agentic AI Foundation (Linux Foundation 산하)** 에 기증. 공동 창립: Anthropic·Block·OpenAI, 후원: Google·Microsoft·AWS·Cloudflare·Bloomberg. **Kubernetes·PyTorch·Node.js와 같은 중립 인프라**로 격상.

## 2. 그전에는 어떤 문제가 있었나

LLM이 외부 도구를 쓰려면 *각 도구마다 별도의 통합 코드*를 짜야 했다 (2022~2024년).

- ChatGPT가 GitHub와 연동? ChatGPT용 GitHub 플러그인 별도 작성
- Claude가 Slack과 연동? Claude용 Slack 통합 별도 작성
- 같은 GitHub인데 *모델마다 다른 코드*

→ **N×M 문제**: 모델 N개 × 도구 M개마다 통합 작성. 100개 도구 × 5개 모델 = 500개 통합.

**일상 비유**: 옛날 휴대폰 시대, 충전기가 회사마다 달랐다. 노키아 핀, 삼성 24핀, 애플 30핀, 마이크로 USB, 미니 USB… 가방에 충전기 5개를 들고 다녀야 했다. **USB-C가 등장하면서 *한 개*로 끝**난 것과 정확히 같은 일이 LLM-도구 연결에서 일어났다.

## 3. 어떻게 해결했나

MCP는 **클라이언트(=LLM 호스트)와 서버(=도구) 사이의 표준 메시지 형식**을 정한 프로토콜.

```text
[LLM 호스트]                    [MCP 서버]
 Claude / GPT / Gemini  ←━━━━━━━━━  GitHub 서버
                       ←━━━━━━━━━  Slack 서버
                       ←━━━━━━━━━  Figma 서버
                       ←━━━━━━━━━  Postgres 서버
                                   ... 누구나 만들 수 있음
```

- 도구를 만드는 쪽: **MCP 서버 한 번만** 만들면 모든 LLM에서 쓰임
- LLM을 만드는 쪽: **MCP 클라이언트 한 번만** 구현하면 모든 도구를 쓸 수 있음
- N+M으로 떨어진다.

### 채택 타임라인

- **2024-11**: Anthropic 공개
- **2025 Q2**: OpenAI가 ChatGPT의 Apps SDK·Connectors를 통해 MCP 지원
- **2025 Q3**: Microsoft가 GitHub·Azure·Teams·M365 MCP 서버 출시
- **2025-12**: Anthropic이 Agentic AI Foundation에 MCP 기증
- **2026 Q1**: Google이 Gemini API·Vertex AI Agent Builder에 MCP 지원
- **2026-03 기준**: 공개 MCP 서버 **10,000개 이상**, 월 SDK 다운로드 **9,700만 회** (Python·TypeScript 합계)
- **2026 Q1**: 엔터프라이즈 AI 팀(50+ ML 인력 보유) 중 **78%**가 *프로덕션에 MCP 기반 에이전트* 1개 이상 운영 (1년 전 31% 대비 큰 증가)

## 라이브 시연 가능한 예시

### 시연 1 — Figma MCP로 디자인 → 코드
```bash
[Claude Code 안에서]
> 이 Figma 페이지의 컴포넌트를 React로 만들어줘
  https://figma.com/design/abc123/...

[자동 처리]
1. Figma MCP 서버 호출 → 디자인 메타데이터·스크린샷 가져옴
2. Claude가 코드로 변환
3. 결과 출력
```
청중에게 이 순간을 보여주면 *"AI가 외부 세상과 연결됐다"* 가 한 번에 와닿는다.

### 시연 2 — 같은 도구를 다른 모델에서 호출
```bash
[Claude Code]
> /mcp__github__list_issues  → 이슈 목록 표시

[ChatGPT 데스크톱]
> /mcp__github__list_issues  → 같은 결과 (같은 MCP 서버 사용)
```
**같은 MCP 서버**를 두 모델이 공유한다는 사실 자체가 청중에게 *프로토콜의 힘*을 느끼게 한다.

## Before/After — MCP 유무

| 측면 | MCP 없음 (2024 이전) | MCP 있음 (2026) |
|---|---|---|
| 도구 N개 × 모델 M개 통합 | N × M 개 코드 작성 | N + M 개 코드만 |
| 새 도구 추가 | 모델마다 별도 통합 | MCP 서버 1번 작성 → 모든 모델에서 사용 |
| 새 모델 출시 | 모든 도구 통합 다시 작성 | MCP 클라이언트 1번 구현 → 기존 도구 즉시 사용 |
| 표준화 | 없음 — 도구마다 형식 다름 | RFC 수준 명세, 검증된 SDK |

## 실제 사례

- **Figma**: 공식 MCP 서버. 디자인 파일에서 메타데이터·스크린샷·Code Connect 매핑 가져오기
- **Google Drive·Gmail·Calendar**: 모두 MCP 서버 형태로 제공. Claude·ChatGPT·Gemini에서 동일하게 호출 가능
- **GitHub**: 이슈·PR·코드 검색·CI 상태 조회 가능
- **Postgres·Puppeteer·Slack**: Anthropic이 출시 직후 직접 작성한 reference servers

## 1·2강 강의 연결 포인트

- **1강 #23** [데모: 23-mcp-extensions.html] — 정확히 이 문서의 도입부. *"이런 게 있다 정도만 알아두시면 된다"* 수준에서 짧게 언급. 이 문서는 그 *깊이 있는 보완*.
- **1·2강 모두**: MCP는 직접 실습엔 안 등장하지만, 강의자가 *"외부 세상과 어떻게 연결되는가"* 질문을 받았을 때 답할 수 있어야 한다.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code](Claude-Code.md) — MCP 클라이언트의 대표적 구현
- [서브에이전트](서브에이전트.md) — MCP와 함께 자주 등장하는 *외부 능력 확장* 메커니즘 (둘은 다른 축: MCP=외부 도구, 서브에이전트=내부 분업)
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — MCP는 컨텍스트 엔지니어링의 *외부 컨텍스트* 공급 표준
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — MCP는 하니스의 *외부 도구 연결* 레이어

## 출처

- [Anthropic — Introducing the Model Context Protocol (2024-11)](https://www.anthropic.com/news/model-context-protocol) — 공식 발표
- [Anthropic — Donating MCP and establishing the Agentic AI Foundation (2025-12)](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) — Linux Foundation 기증 발표
- [Wikipedia — Model Context Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol) — 정의·역사·채택 정리
- [Model Context Protocol Specification (2025-11-25)](https://modelcontextprotocol.io/specification/2025-11-25) — 최신 스펙
- [DigitalApplied: MCP Adoption Statistics 2026](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol) — 채택률·서버 수치
- [SurePrompts: MCP Complete 2026 Guide](https://sureprompts.com/blog/model-context-protocol-mcp-complete-guide-2026) — 사용 사례 모음
