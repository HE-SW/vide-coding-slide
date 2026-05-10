# 왜 CLI인가 — Claude Code의 디자인 선택

> 비개발자 청중이 가장 먼저 던지는 질문: *"왜 까만 화면이어야 해요? 그냥 채팅창에서 쓰면 안 되나요?"* 청중이 Claude Code 앞에서 위축되지 않게 만들어주는 핵심 슬라이드.

## 1. CLI가 뭔가 (한 문단)

- **CLI (Command Line Interface)**: 마우스로 버튼을 누르는 게 아니라 **글자로 명령을 입력해 컴퓨터를 다루는 방식**. 흔히 보는 까만 창(터미널). Windows의 `cmd`, macOS·Linux의 `Terminal`이 그것.
- **GUI (Graphical User Interface)**: 우리가 일상에서 쓰는 거의 모든 화면 — 아이콘·창·버튼.
- 둘은 **상극이 아니라 도구의 종류 차이**. 같은 일을 다른 방식으로 시킬 뿐이다.

## 2. claude.ai 채팅 vs Claude Code CLI — 무엇이 다른가

청중이 이미 알고 있을 비교 대상은 **claude.ai 웹 채팅**. 둘 다 같은 Claude 모델을 쓰지만 **할 수 있는 일의 범위**가 다르다.

| 기능 | claude.ai (웹 채팅) | Claude Code (CLI) |
|---|---|---|
| 글로 묻고 답 받기 | ✅ | ✅ |
| 내 컴퓨터 파일 읽기 | ❌ (직접 붙여넣기 필요) | ✅ |
| 내 컴퓨터 파일 수정·저장 | ❌ | ✅ |
| 명령 실행(빌드/테스트/git) | ❌ | ✅ |
| 작업을 자동화/반복 | ❌ | ✅ |
| 여러 도구 연결 (MCP) | 일부 | ✅ |
| 결과를 다른 프로그램에 흘려보내기 | ❌ | ✅ |

→ **챗봇이 "조언자"라면 CLI는 "동료 개발자"** — 직접 손을 움직여 작업을 해준다.

## 3. 왜 Anthropic은 CLI를 골랐나

Anthropic의 공식 표현: *"do the simple thing first"* — 모델 능력을 가장 얇은 껍데기로 노출.

### (1) 파일 시스템과 명령 실행이 자연스러움
- 코딩의 진짜 작업은 *대화*가 아니라 *파일을 읽고, 고치고, 실행*하는 것.
- 터미널은 그 셋이 모두 1초 안에 일어나는 환경. CLI 도구는 같은 자리에서 같은 권한으로 동작.

### (2) 조립(composable)이 쉽다
- CLI는 **유닉스 철학**(작은 도구를 파이프로 이어 큰 일을 한다)에 잘 맞는다.
- `git diff | claude "리뷰해줘"`처럼 다른 명령의 출력을 그대로 입력으로 전달 가능.
- CI/CD(자동 빌드·배포 파이프라인)에 끼워넣기 쉽다 — 결국 둘 다 명령줄에서 돌아간다.

### (3) 어디서나 동일하게 동작
- macOS·Linux·Windows·서버·도커 컨테이너… **터미널이 있는 곳이면 어디든**.
- IDE(VS Code, JetBrains)에 종속되지 않으므로, 청중이 어떤 환경을 쓰든 강의 내용이 그대로 적용됨.

### (4) 내 컴퓨터 안에서 동작
- 파일 업로드·다운로드 없이 **현재 폴더에서 즉시 작업**.
- 회사 코드를 외부 웹 서비스에 올리지 않아도 된다는 보안적 이점.

### (5) 자동화·반복
- 정해진 시간에 자동 실행, 여러 작업을 동시에 병렬 실행, 같은 작업을 100번 반복…
- GUI 채팅창에서는 매번 사람이 클릭해야 하는 일들을 **스크립트로 묶어둘 수 있다**.

## 4. 비개발자에게 어떻게 설명할까 (강의용 비유)

| 비유 | 메시지 |
|---|---|
| **레스토랑 vs 주방** | 채팅창은 손님이 주문하는 *홀*. CLI는 주방 — 직접 재료를 만지고, 불을 켜고, 그릇에 담는다. |
| **음성 비서 vs 비서 직원** | "Siri야, 회의 잡아줘"는 채팅. *비서가 내 책상에 앉아 직접 일정·메일·문서를 다루는 것*은 CLI. |
| **요리 레시피 vs 도시락 배달** | claude.ai는 레시피만 알려준다. Claude Code는 *재료까지 사 와서 만들어 식탁에 올려준다*. |

청중이 가장 잘 받는 건 보통 첫 번째(레스토랑/주방) 비유.

## 5. CLI 문턱이 낮아지고 있다 (덧붙이는 안심 메시지)

비개발자 청중이 까만 화면을 무서워하지 않게 깔아주면 좋은 사실:

- 기억할 명령은 거의 없다 — Claude Code는 한국어/영어로 **자연어**를 그대로 받는다. `cd`, `ls` 같은 명령은 안 외워도 된다.
- 잘못 입력해도 컴퓨터가 망가지지 않는다 — `/sandbox` 모드, `/permissions` 권한 시스템이 위험한 명령을 자동 차단.
- 잘못 결정한 건 [`/rewind`](Claude-Code.md#-세션-관리)로 시점 단위로 되돌릴 수 있다.

## 강의 연결 포인트

- [Claude Code](Claude-Code.md) 슬라이드 직전·직후에 배치.
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) 메시지의 **현실 사례** — "도구를 쥐여주는 환경"이 곧 CLI다.
- 강의 핵심 메시지 *"좋은 결과는 우연이 아니라 설계"* — CLI는 *반복·자동화·검증*을 가능하게 하는 무대. 채팅창은 이걸 못 한다.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code](Claude-Code.md) — CLI로 구현된 바이브코딩 도구의 대표 사례
- [CLAUDE.md](CLAUDE-md.md) — CLI 환경에서 컨텍스트를 영속시키는 파일
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — CLI가 자연스러운 무대인 이유
- [바이브코딩](../concepts/바이브코딩.md) — Karpathy 본인은 음성 입력+CLI 조합을 묘사

## 출처

- [Claude Code | Anthropic 공식 제품 페이지](https://www.anthropic.com/product/claude-code) — Anthropic의 공식 포지셔닝
- [Claude Code CLI Reference — Anthropic Docs](https://code.claude.com/docs/en/cli-reference) — CLI 명령 전체
- [CLI-First Agency: Why Claude Code Lives in Your Terminal — SitePoint](https://www.sitepoint.com/claude-code-cli-agent-review/) — CLI 우선 디자인 분석
- [Inside Claude Code: A Deep Dive into Anthropic's Agentic CLI Assistant — John Ding](https://medium.com/@dingzhanjun/inside-claude-code-a-deep-dive-into-anthropics-agentic-cli-assistant-a4bedf3e6f08) — 아키텍처 해설
- [Claude Code Explained: How Anthropic's Terminal-First Coding Agent Works — DataStudios](https://www.datastudios.org/post/claude-code-explained-how-anthropic-s-terminal-first-coding-agent-works-across-cli-sessions-ide-in) — terminal-first 철학 정리
