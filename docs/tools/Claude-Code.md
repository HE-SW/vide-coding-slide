# Claude Code 명령어 (Slash Commands)

> **2026-05-07 기준, Claude Code 2.x 계열 최신 버전.**
> 사용자가 받은 1.0.73 기준 자료를 현재 버전으로 갱신한 결과. 강의 중 청중이 "그 명령어 아직 쓸 수 있나요?" 같은 질문을 했을 때 강의자가 즉시 답할 수 있도록 정리했다.

## Claude Code란

터미널에서 자연어로 코드를 짜고, 파일을 고치고, 명령을 실행해주는 Anthropic 공식 CLI 도구. "바이브코딩"의 대표적 구현체 중 하나로, 1강에서 다루는 **하니스 엔지니어링**의 좋은 예시이기도 하다 (LLM이 단순히 답만 뱉는 게 아니라, 도구를 쓰고 결과를 보고 다시 시도하는 반복 루프를 갖춤).

명령어는 `/`로 시작하는 슬래시 커맨드로 호출한다. 예: `/help`.

---

## 1.0.73 → 현재 버전 변경 요약

### 삭제된 명령어
- ❌ `/pr-comments` — `/review`로 대체
- ❌ `/vim` — `/config`의 Editor mode로 이동
- ❌ `/migrate-installer` — 2.x에서 더 이상 필요 없음

### 별칭(alias) 정리
- `/cost` → 이제 `/usage`의 별칭
- `/bug` → `/feedback`의 별칭
- `/clear` → `/reset`, `/new` 추가
- `/resume` → `/continue` 추가
- `/exit` → `/quit` 추가
- `/config` → `/settings` 추가
- `/permissions` → `/allowed-tools` 추가

### 신규 명령어 (대표적 30+개)
컨텍스트/체크포인트/계획/효율 모드 같은 **작업 관리** 기능과, 클라우드/모바일/팀 협업 관련 명령어가 대거 추가됐다. 자세한 항목은 아래 섹션 참고.

---

## 🔄 세션 관리

| 명령어 | 설명 |
|---|---|
| `/clear` | 대화 기록 완전 삭제. (별칭: `/reset`, `/new`) |
| `/compact [지시]` | 대화를 요약해 토큰 절약. 예: `/compact 핵심 코드 변경만 남겨줘` |
| `/resume` | 이전 세션 목록에서 골라 이어가기. (별칭: `/continue`) |
| `/exit` | 세션 종료. (별칭: `/quit`) |
| 🆕 `/rewind` | 대화를 특정 시점으로 되돌리기 / 체크포인트. (별칭: `/checkpoint`, `/undo`) |
| 🆕 `/branch` | 현재 대화에서 갈래를 쳐서 새 흐름 시작. (별칭: `/fork`) |
| 🆕 `/rename` | 현재 세션 이름 바꾸기 |
| 🆕 `/recap` | 세션을 한 줄로 요약 |

## 🏗️ 프로젝트 초기화

| 명령어 | 설명 |
|---|---|
| `/init` | 현재 프로젝트를 분석해 `CLAUDE.md`(프로젝트 메모리)를 생성 |
| `/add-dir` | 작업 디렉토리 추가. 예: `/add-dir ../libs ../docs` |

## 👤 계정

| 명령어 | 설명 |
|---|---|
| `/login` | Anthropic 계정 로그인 (브라우저 인증) |
| `/logout` | 로그아웃 |
| `/upgrade` | Max 플랜 업그레이드 |
| 🆕 `/extra-usage` | 사용 한도 초과 시 결제 옵션 설정 |
| 🆕 `/privacy-settings` | 데이터 사용 관련 프라이버시 설정 (Pro/Max 전용) |

## ⚙️ 시스템 / 진단

| 명령어 | 설명 |
|---|---|
| `/doctor` | 설치/설정 상태 종합 점검 |
| `/status` | 버전·모델·계정 등 현재 상태 표시 |
| `/config` | 설정 패널 열기. (별칭: `/settings`) — Vim 모드도 여기서 |
| `/help` | 명령어 도움말 |
| 🆕 `/context` | 현재 컨텍스트 사용량을 색상 격자로 시각화 |
| 🆕 `/usage` | 비용·플랜 한도·활동 통계. 기존 `/cost`가 이쪽으로 통합 |
| 🆕 `/stats` | `/usage`의 Stats 탭 별칭 |
| 🆕 `/insights` | 세션 분석 리포트 |
| 🆕 `/heapdump` | 메모리 덤프 (디버깅용) |

## 🎨 UI / 입력

| 명령어 | 설명 |
|---|---|
| `/statusline` | 터미널 하단 상태 표시줄 설정 |
| `/terminal-setup` | Shift+Enter 줄바꿈 키바인딩 등 터미널 편의 설정 |
| 🆕 `/theme` | 색상 테마 변경 |
| 🆕 `/color` | 프롬프트 바 색상 |
| 🆕 `/tui` | 터미널 UI 렌더러 전환 |
| 🆕 `/keybindings` | 키바인딩 설정 |
| 🆕 `/focus` | 포커스 뷰 토글 (도구 호출 숨기고 결과만 표시) |
| 🆕 `/voice` | 음성 입력 토글 |
| 🆕 `/copy` | 응답을 클립보드에 복사 |
| 🆕 `/diff` | 미커밋 변경/턴별 diff 인터랙티브 뷰어 |

## 🔧 개발 도구 연동

| 명령어 | 설명 |
|---|---|
| `/ide` | VS Code / JetBrains 연결 상태 |
| `/mcp` | Model Context Protocol 서버 관리. 예: `/mcp` 후 GitHub·Figma 등 외부 도구 연결 |
| 🆕 `/plugin` | 플러그인 관리 |
| 🆕 `/reload-plugins` | 플러그인 리로드 |
| 🆕 `/skills` | 사용 가능한 Skill 목록/관리 |
| 🆕 `/chrome` | Chrome 통합 설정 |
| 🆕 `/sandbox` | 샌드박스 모드 토글 (위험한 명령 자동 차단) |

## 🐙 GitHub / 협업

| 명령어 | 설명 |
|---|---|
| `/install-github-app` | 저장소에 Claude GitHub Actions 설치 |
| `/review` | PR 코드 리뷰. 예: `/review #456` |
| `/security-review` | 현재 브랜치 보안 취약점 검사 |
| 🆕 `/install-slack-app` | Slack 통합 |
| 🆕 `/autofix-pr` | PR 이슈 자동 수정 |
| 🆕 `/ultrareview` | 멀티 에이전트 클라우드 기반 심층 PR 리뷰 (사용자만 실행 가능, 별도 과금) |
| 🆕 `/web-setup` | 웹 버전과 GitHub 연결 |

## 🛡️ 권한·메모리·후크

| 명령어 | 설명 |
|---|---|
| `/permissions` | 도구 권한 허용/거부 규칙. (별칭: `/allowed-tools`) |
| `/hooks` | 도구 이벤트 훅 (예: 파일 저장 시 자동 실행 스크립트) |
| `/memory` | `CLAUDE.md` 등 메모리 파일 편집 |
| 🆕 `/fewer-permission-prompts` [Skill] | 권한 프롬프트 줄이기 |

## 🤖 모델 / 실행 모드

| 명령어 | 설명 |
|---|---|
| `/model` | 사용 모델 변경 (Sonnet / Opus / Haiku) |
| 🆕 `/effort` | 모델 노력 수준 (low → max) |
| 🆕 `/fast` | Fast 모드 토글 (Opus 4.6에서 출력 속도 우선) |
| 🆕 `/plan` | Plan 모드로 진입 (실행 전 계획 수립) |

## 🤝 에이전트 / 자동화 / Skill

| 명령어 | 설명 |
|---|---|
| `/agents` | 서브에이전트 구성 관리 |
| 🆕 `/loop` [Skill] | 일정 간격으로 같은 프롬프트 반복 실행 |
| 🆕 `/schedule` [Skill] | 정기 작업(루틴) 생성·실행 |
| 🆕 `/batch` [Skill] | 대규모 변경을 병렬 실행 |
| 🆕 `/debug` [Skill] | 디버그 로깅 활성화 |
| 🆕 `/simplify` [Skill] | 코드 리뷰 & 단순화 |
| 🆕 `/claude-api` [Skill] | Claude API 레퍼런스 / 마이그레이션 가이드 |

## 📊 데이터 / 세션 관리

| 명령어 | 설명 |
|---|---|
| `/export` | 대화를 파일/클립보드로 내보내기. 예: `/export conversation.md` |
| `/bashes` | 백그라운드 bash 프로세스 목록. (별칭: `/tasks`) |
| 🆕 `/btw` | 컨텍스트 오염 없이 잠깐 다른 질문 |

## 📱 멀티 디바이스 / 원격

| 명령어 | 설명 |
|---|---|
| 🆕 `/desktop` | 데스크톱 앱에서 이어서 작업. (별칭: `/app`) |
| 🆕 `/mobile`, `/ios`, `/android` | 모바일 앱 QR 코드 표시 |
| 🆕 `/teleport` | 웹 세션을 터미널로 가져오기. (별칭: `/tp`) |
| 🆕 `/remote-control` | claude.ai에서 원격 제어. (별칭: `/rc`) |
| 🆕 `/remote-env` | 기본 원격 환경 설정 |
| 🆕 `/ultraplan` | 브라우저에서 계획 작성 |

## ☁️ 클라우드 제공자 설정

| 명령어 | 설명 |
|---|---|
| 🆕 `/setup-bedrock` | AWS Bedrock 설정 |
| 🆕 `/setup-vertex` | Google Vertex AI 설정 |

## 👥 팀 / 학습

| 명령어 | 설명 |
|---|---|
| 🆕 `/team-onboarding` | 팀원 온보딩 가이드 |
| 🆕 `/powerup` | 인터랙티브 기능 학습 |

## ℹ️ 기타 / 메타

| 명령어 | 설명 |
|---|---|
| `/release-notes` | 최신 릴리스 노트 |
| `/feedback` | 피드백/버그 제출. (별칭: `/bug`) — 현재 대화도 첨부됨 |
| 🆕 `/passes` | 친구에게 무료 1주 패스 공유 |
| 🆕 `/stickers` | 스티커 주문 |

---

## 강의용 추천 시연 흐름

비개발자 청중에게 보여줄 때, 한 번에 다 보여주지 말고 **3개 그룹**으로 묶어서 시연하면 흐름이 잘 살아난다.

1. **"기본 사용감"** (5분): `/help` → `/init` → 자연어로 한 가지 요청 → `/clear`
   - 청중이 가장 먼저 머리에 그려야 할 것: "터미널에 영어/한국어로 부탁하면 답해주는 도구"

2. **"되돌리기와 다시 시도"** (5분): `/rewind` → `/branch` → `/compact`
   - 1강 핵심 메시지 "AI는 한 번에 안 된다, 반복하는 게 정상이다"와 직접 연결되는 부분.

3. **"확장의 가능성"** (3분): `/mcp`, `/agents`, `/install-github-app`만 이름과 한 줄 설명
   - 깊이 안 들어가도 됨. "이 도구가 단순 챗봇이 아니라 다른 시스템과 연결된다는 인상"만 남기면 충분.

---

## 꼬리에 꼬리 (관련 개념)

- [바이브코딩](../concepts/바이브코딩.md) — Claude Code는 바이브코딩의 대표 구현체
- [왜 CLI인가](CLI를-쓰는-이유.md) — claude.ai 채팅 대신 CLI를 고른 이유
- [CLAUDE.md](CLAUDE-md.md) — `/init`이 만들고 `/memory`가 편집하는 프로젝트 메모리 파일
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — `/agents`, `/sandbox`, `/hooks`가 LLM에 "도구를 안전하게 쥐여주는" 방식
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — `/context`, `/compact`, `/memory`가 컨텍스트 관리의 실전 도구
- [프롬프트 엔지니어링](../techniques/프롬프트-엔지니어링.md) — Slash Command 자체가 사전 정의된 프롬프트 템플릿

---

## 출처

- Claude Code 공식 명령어 문서 (Anthropic Docs): https://docs.anthropic.com/en/docs/claude-code/slash-commands
- Claude Code 릴리스 노트: https://github.com/anthropics/claude-code/releases
- 본 문서 작성 시점에 Claude Code 내장 가이드 에이전트(`claude-code-guide`)로 직접 교차 검증.

> ⚠️ Claude Code는 빠르게 업데이트된다. 강의 직전에 `/release-notes`로 최신 변경사항을 한 번 더 확인할 것.
