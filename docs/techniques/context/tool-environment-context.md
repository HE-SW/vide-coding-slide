# Tool & Environment Context (도구·환경 컨텍스트)

> 모델이 **자기 행동의 결과**·**현재 환경**을 *다시 보는* 영역. 도구 호출 결과·시각·OS·디렉토리 같은 *세계의 상태*가 컨텍스트로 들어온다.

> 부모 문서: [컨텍스트 엔지니어링](../컨텍스트-엔지니어링.md)

## 1. 정의

두 가지 결합:
- **Tool Context** — 모델이 *호출한 도구의 결과*가 다시 컨텍스트로 들어옴 (자세히는 [Tool Use](../../concepts/Tool-Use.md))
- **Environment Context** — *현재 시각·OS·작업 디렉토리·플랫폼·환경 변수* 같은 *세계 상태*

## 2. 그전에는 어떤 문제가 있었나

LLM이 *행동*을 할 수 있게 됐는데 (tool use 등장) — *행동 후에 무엇이 일어났는지* 모델에게 다시 알려주는 표준이 없었다.

- *"파일 읽어줘"* → 도구 실행 → 결과는 어디로?
- *"오늘 날짜 알아?"* → 모델은 학습 컷오프만 알고 *진짜 오늘*을 모름
- *"이 폴더 정리해줘"* → 어떤 폴더? *현재 작업 디렉토리*가 컨텍스트에 없으면 추측

→ *행동 결과*와 *환경 정보* 를 모델에 주입하는 매커니즘이 필요했다.

**일상 비유**: 회의실에 들어선 컨설턴트. *"지금 몇 시인가요? 우리 어디에 있나요?"* 같은 *현장 정보*가 없으면 — 좋은 조언을 못 한다. Tool & environment context가 그 *현장 정보*.

## 3. 두 축 자세히

### (A) Tool Context — 도구 결과의 피드백 루프

```text
[Turn 1]
모델 출력:  Bash 도구 호출 → "ls -la"
시스템:     도구 실행 → "drwxr-xr-x  3 user  ... README.md ..."
            ↓ (결과를 모델 입력으로 다시)

[Turn 2 — 같은 응답 안에서 계속]
모델 입력:  [도구 호출] + [도구 결과]
모델 출력:  "이 디렉토리에 README.md 가 있네요. 다음으로..."
```

→ 모델은 *자기 행동의 결과*를 보고 다음 행동을 결정. 이 *루프*가 에이전트의 본질.

**Tool context의 형태**:
- Bash 명령 stdout/stderr
- 파일 읽기 결과
- API 응답 JSON
- 검색 결과 (Web Search 도구)
- 코드 실행 결과 (파이썬 인터프리터)

### (B) Environment Context — 세계 상태

매 세션 시작 시 자동 주입되는 정보. Claude Code의 경우:

```text
- 현재 작업 디렉토리: /Users/khaneol/.../vide-coding-presentation
- Git 저장소: yes (브랜치: main)
- 플랫폼: darwin
- Shell: zsh
- OS Version: Darwin 25.3.0
- 오늘 날짜: 2026-05-10
- Claude 모델: claude-opus-4-7
```

→ 모델은 이 정보를 알고 *맥락에 맞는 답*을 한다. *"오늘 날짜 알아?"* 에 답할 수 있는 이유.

## Before / After

```text
[BEFORE — environment context 없음]
USER: "이 폴더에 .gitignore 추가해줘"
AI:   "어느 폴더에 추가할까요? 절대경로를 알려주세요."

[AFTER — Claude Code의 자동 environment context]
USER: "이 폴더에 .gitignore 추가해줘"
AI:   [작업 디렉토리 자동 인식]
      "현재 디렉토리(.../vide-coding-presentation)에 추가합니다."
      → Write 도구 호출 → 즉시 생성
```

## 라이브 시연 가능한 예시

### 시연 1 — 환경 정보 묻기
```bash
> "지금 몇 시야?"
AI:   "환경 정보에 따르면 2026-05-10 입니다.
       시간대는 시스템에 명시 안 됨."

> "이 디렉토리 어디야?"
AI:   "/Users/khaneol/DEEPNOID/AX/vide-coding-presentation 입니다."
       (= environment context 자동 활용)
```

### 시연 2 — 도구 결과 루프 (Tool context)
```bash
USER: "이 레포 파이썬 파일 모두 찾아서 가장 큰 거 알려줘"

[Claude의 내부 루프]
🔧 Bash: find . -name "*.py" -exec wc -l {} \;
   결과: scripts/score.py 423줄 / utils.py 89줄 / ...
   ↓ (Tool context로 재주입)
🔧 Bash: 결과 파싱
   ↓
"가장 큰 파일은 scripts/score.py 423줄."
```

→ 같은 응답 안에서 *도구 호출 → 결과 → 다음 호출* 의 루프. **이게 agentic 동작의 본질**.

## 4. 실제 사례 (2026)

- **Claude Code 자동 environment context**: 세션 시작 시 작업 디렉토리·git 상태·플랫폼·OS 자동 주입.
- **MCP의 `resources`**: 외부 시스템의 *현재 상태*를 표준화된 컨텍스트로 (예: Linear의 *현재 활성 이슈 목록*).
- **Cursor의 인덱스**: 코드베이스 구조를 백그라운드에서 인덱싱 → environment context로 *항상 사용 가능*.
- **OpenAI o-series**: *"reasoning trace"* 도 일종의 self-tool context — 자기 추론 결과를 다시 보면서 답.

## 한계와 주의

- **Tool context 폭증**: 도구 결과가 길면 (예: 10MB 로그) — 컨텍스트 창 폭증. *요약·필터링* 필요.
- **Environment 변경**: 사용자가 `cd` 로 디렉토리 바꾸면 — 모델은 *다음 응답에야* 인지. 시점 차이 주의.
- **민감한 환경 정보**: 환경 변수에 *비밀번호·API 키* 가 있으면 — 시스템이 모델 입력에서 *마스킹*해야 함.

## 꼬리에 꼬리 (관련 개념)

- [컨텍스트 엔지니어링](../컨텍스트-엔지니어링.md) — 부모 문서
- [System / Conversation / Knowledge Context](../컨텍스트-엔지니어링.md) — 다른 레이어들
- [Tool Use](../../concepts/Tool-Use.md) — Tool context의 발생 매커니즘
- [MCP](../../tools/MCP.md) — Tool & resource context 의 표준 프로토콜
- [Claude Code Headless 모드](../../tools/Claude-Code-Headless-모드.md) — environment context 가 매번 *새로* 주입되는 환경

## 출처

- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 공식
- [Anthropic — Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — Tool context 매커니즘
- [LangChain — Context Engineering](https://docs.langchain.com/oss/python/langchain/context-engineering) — environment context 패턴
