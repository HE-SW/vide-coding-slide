# Claude Code Plugin (플러그인)

> **Skills + Hooks + MCP 서버 + 서브에이전트**를 한 묶음으로 패키징한 **설치 단위**. *"이 프로젝트엔 풀세팅이 필요해"* 의 답. `/plugin install` 한 줄로 끝. 2025년 후반에 추가된 Claude Code 확장의 *최상위 단위*.

## 1. 왜 "Plugin"이라고 부르나

- 영어 *Plug + in*. 기존 시스템에 *꽂아* 기능을 더한다는 표준 컴퓨팅 용어 (브라우저 플러그인, IDE 플러그인 등).
- **Claude Code 플러그인의 정체**: 마크다운·설정 파일들을 묶은 폴더. 안에 들어가는 것:
  - 1개 이상의 **Skill** (`/이름` 호출)
  - 0개 이상의 **Hook** (이벤트 자동 발화)
  - 0개 이상의 **MCP 서버** 설정
  - 0개 이상의 **서브에이전트**

→ **하나의 plugin은 하나의 *완성된 워크플로우 패키지*** 다.

- **언제 등장**: Claude Code 출시(2025-02) 후 점진 추가. 2025년 후반에 *공식 마켓플레이스* `claude-plugins-official` 출범, **2026-03 기준 101개**.

## 2. 그전에는 어떤 문제가 있었나

Skill 하나·Hook 하나만으로는 *완성된 워크플로우*가 안 됐다.

- Skill만 깔면 → 호출은 되지만 *자동 검증 루프*는 없음
- Hook만 깔면 → 자동 후처리는 되지만 *워크플로우 시작점*이 없음
- MCP만 깔면 → 외부 도구 호출은 되지만 *언제·어떻게* 부를지 모름
- 사용자가 **여러 조각을 직접 조립**해야 했음 → 진입 장벽

→ *"하나의 검증된 워크플로우"* 를 *한 번에 깔고 한 번에 지울 수 있는* 단위가 필요했다.

**일상 비유**: 휴대폰 앱은 *하나의 기능*이 아니라 *여러 기능의 묶음*. 카카오톡은 *메시지 + 전화 + 결제 + 미니앱*. plugin은 *Claude Code 안의 앱*에 가깝다.

## 3. 어떻게 해결했나 — 묶음 + 마켓플레이스

### Plugin 구조

```text
my-plugin/
├── .claude-plugin/
│   ├── manifest.json        ← plugin 메타데이터
│   └── marketplace.json     ← (마켓플레이스용)
├── skills/                  ← 1개+
│   └── plan-and-build/
│       └── SKILL.md
├── agents/                  ← 0개+ 서브에이전트
│   └── code-reviewer.md
├── hooks/                   ← 0개+ 훅
│   └── pre-commit.sh
└── settings.json            ← 0개+ MCP 서버 / hook 등록
```

### 설치 방법

```bash
# 1) Anthropic 공식 마켓플레이스 — 자동 등록됨
/plugin install my-workflow@claude-plugins-official

# 2) 커뮤니티 마켓플레이스 추가 후
/plugin marketplace add owner/repo
/plugin install plugin-name@owner-repo

# 3) Discover 탭에서 GUI로 탐색
/plugin
```

설치 후엔 **`/plugin list`** 로 활성 plugin 확인, **`/plugin remove`** 로 제거.

### 마켓플레이스 — 어디서 받는가

플러그인의 *유통 레이어*. 공식 카탈로그(`claude-plugins-official`)는 자동 활성화돼 있어 `/plugin install <name>@claude-plugins-official` 만으로 깔리고, 커뮤니티·사내 사설 카탈로그는 `/plugin marketplace add` 로 등록한다. **어디서 찾는지·어떻게 추가하는지·실제 카탈로그 목록**은 [Plugin Marketplace](Plugin-Marketplace.md) 문서 참조.

## Skills vs Plugins — 한 줄 차이

```text
Skill   = 한 가지 작업 절차 (`/이름` 한 줄)
Plugin  = Skill + Hook + MCP + Agent 의 *묶음 패키지*
```

→ 비유: **Skill = 책 한 권**, **Plugin = 시리즈 박스세트**.

## Before / After

```text
[BEFORE — 직접 조립]
1주차: skills/ 안에 SKILL.md 직접 작성 (8시간)
2주차: hooks 등록 (5시간)
3주차: 서브에이전트 정의 (4시간)
4주차: MCP 서버 설정 (3시간)
→ 합 20시간, 품질은 사용자 실력에 의존

[AFTER — Plugin]
1분: /plugin install awesome-team-flow
→ 검증된 워크플로우가 *통째로* 깔림
```

## 라이브 시연 가능한 예시

```bash
[강의 중]
> /plugin

[Discover 탭]
- ✅ claude-plugins-official (101개)
  - Knowledge Work — Sales · Marketing · Legal
  - Engineering — TDD Suite · Security Auditor
  ...

> /plugin install tdd-suite@claude-plugins-official

→ 즉시 /tdd-cycle, /tdd-review 같은 슬래시 + tdd-guard hook 작동
```

청중에게 *"한 줄 명령에 워크플로우 풀세팅이 깔린다"* 를 직접 시연.

## 강의 연결 포인트

- **모델 한계 섹션**과는 직접 연결되지 않음.
- **`oh-my-claudecode` 풀세팅 슬라이드** [데모: 05-oh-my-claudecode.html] — `oh-my-claudecode` 자체가 *plugin의 거대 사례*. **32개 전문 에이전트 + Skill 시스템 + 5단계 자동 파이프라인 + HUD + 비용 절감**을 한 묶음으로 제공.
- **범용 하니스 vs 커스텀 하니스 슬라이드** [데모: 06-preset-vs-custom.html] — plugin 은 정확히 *범용 하니스* 쪽의 구현 단위.

## 실제 사례 (2026 베스트)

- **`tdd-suite`**: TDD 강제 워크플로우 + tdd-guard hook + 테스트 러너 자동화
- **`security-suite`**: 보안 감사 서브에이전트 + 위험 명령 차단 hook + OWASP MCP 서버
- **`design-suite`**: 디자인 리뷰 서브에이전트 + Figma MCP + 디자인 시스템 룰
- **`oh-my-claudecode`**: 32개 에이전트 + 자동 파이프라인 (한국 개발자, 풀세팅 슬라이드의 사례)
- **공식 *Knowledge Work* plugin 14종** (2025-말 출시): 영업·법무·HR 등 *비개발자* 대상 — 바이브코딩의 외연 확장 신호

## 꼬리에 꼬리 (관련 개념)

- [Claude Code Skills](Claude-Code-Skills.md) — Plugin 구성 요소 #1
- [Claude Code Hooks](Claude-Code-Hooks.md) — Plugin 구성 요소 #2
- [MCP](MCP.md) — Plugin 구성 요소 #3
- [서브에이전트](서브에이전트.md) — Plugin 구성 요소 #4
- [oh-my-claudecode](oh-my-claudecode.md) — Plugin의 거대 사례
- [Plugin Marketplace](Plugin-Marketplace.md) — Plugin의 *유통 레이어* (어디서 찾고 어떻게 등록하는가)
- [Claude Code](Claude-Code.md) — Plugin 호스트, `/plugin` 명령어 제공

## 출처

- [Anthropic — Discover and install prebuilt plugins (Claude Code Docs)](https://code.claude.com/docs/en/discover-plugins) — 공식 명세
- [GitHub: anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — 공식 마켓플레이스
- [Build with Claude — Plugin Marketplace](https://buildwithclaude.com/) — 검색·탐색 페이지
- [claudemarketplaces.com](https://claudemarketplaces.com/) — Skills · MCP Servers · Plugins 통합 디렉토리
- [Agensi: Claude Code Plugin Marketplace Complete Guide (2026)](https://www.agensi.io/learn/claude-code-plugin-marketplace-guide) — 2026 종합 가이드
- [Build to Launch: Best Claude Code Plugins (2026) — 10 Tested, 4 Worth Keeping](https://buildtolaunch.substack.com/p/best-claude-code-plugins-tested-review) — 검증 후기
- [GitHub: ComposioHQ/awesome-claude-plugins](https://github.com/ComposioHQ/awesome-claude-plugins) — 큐레이션 리스트
- [GitHub: jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) — 가장 큰 컬렉션
