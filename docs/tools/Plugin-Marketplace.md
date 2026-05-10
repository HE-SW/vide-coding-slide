# Plugin Marketplace (플러그인 마켓플레이스)

> Claude Code 플러그인을 *어디서 찾고, 어떻게 등록하고, 어떻게 깔지* 정리. **`/plugin marketplace add owner/repo`** 한 줄이 모든 것의 시작점. Anthropic 공식·커뮤니티 큐레이션·기업 내부 사설 — 세 가지 결이 공존하는 2026년 5월 기준 지도.

## 1. 왜 "Marketplace"라고 부르나

- 영어 *Market + place*. *팔 것을 한자리에 모은 장*. 앱스토어·플레이스토어·VS Code Marketplace가 같은 계열.
- **Claude Code의 마켓플레이스**: 플러그인을 모아 *목록(catalog)* 으로 정리한 곳. 정체는 깃 저장소 안의 `.claude-plugin/marketplace.json` 파일 하나, 또는 그 JSON을 호스팅한 URL.
- 사용자는 *마켓플레이스를 한 번 등록*해두면, 그 안의 플러그인을 *언제든 골라 깔 수* 있다.
- **언제 등장**: Claude Code 플러그인 시스템은 2024~2026년 사이 점진적으로 추가됐다. 2025년 후반 Anthropic 공식 카탈로그 `claude-plugins-official` 출범, 2026년 5월 기준 *공식 카탈로그 + 커뮤니티 디렉토리 + 사설 내부 카탈로그* 세 결이 자리잡음.

## 2. 그전에는 어떤 문제가 있었나

플러그인이라는 *묶음 단위*만 있고 *유통 경로*가 없다면, 사용자는 매번 두 가지 고생을 해야 했다.

- **발견 고생**: GitHub을 직접 뒤져 "Claude Code plugin"을 검색 → 어떤 게 신뢰할 만한지 *스스로 판단*
- **설치 고생**: `git clone` → 폴더 위치 옮기기 → `settings.json` 수동 수정 → 재시작

→ 결국 *플러그인을 안 쓰게 되는* 결말. 좋은 패키지는 만들어졌는데 *닿지 않는다*.

**일상 비유**: 모바일 앱이 처음 나왔을 때를 생각하면 됨. 2008년 이전엔 휴대폰에 앱을 깔려면 *제조사 사이트에서 .sis 파일을 받아 PC로 옮기고, 케이블로 꽂아 설치*해야 했다. **앱스토어가 등장하면서 "검색 → 한 번 탭"** 으로 끝나게 됐다. 마켓플레이스가 플러그인에게 한 일이 정확히 같다.

## 3. 어떻게 해결했나 — `/plugin marketplace add`

### 마켓플레이스의 정체

```text
my-marketplace/                         ← 깃 저장소 하나
└── .claude-plugin/
    └── marketplace.json                ← 플러그인 목록·메타데이터
```

`marketplace.json`엔 *어떤 플러그인이 있고, 각각 어디 있는지* 만 적혀 있음. **플러그인 자체는 다른 저장소에 있어도 됨** — 마켓플레이스는 *카탈로그*, 플러그인은 *상품*.

### 추가하는 4가지 경로

```bash
# 1) GitHub 저장소 (가장 흔함)
/plugin marketplace add anthropics/claude-plugins-official

# 2) 다른 깃 호스트 — GitLab·Bitbucket·사내 Git 서버
/plugin marketplace add https://gitlab.com/our-team/plugins.git
/plugin marketplace add git@gitlab.com:our-team/plugins.git#v1.2.0   # 브랜치·태그 핀

# 3) 로컬 디렉토리 — 개발 중·사내 공유 폴더
/plugin marketplace add ./team-marketplace
/plugin marketplace add /Users/me/work/marketplace.json

# 4) 임의 HTTPS URL — 정적 호스팅된 marketplace.json
/plugin marketplace add https://example.com/marketplace.json
```

> 줄여 쓸 수 있음: `/plugin market add ...` 도 동일하게 동작.

### 등록 → 탐색 → 설치 — 3단계

```bash
# 1단계: 카탈로그 등록 (이 시점엔 플러그인이 *깔리진 않음*)
/plugin marketplace add anthropics/claude-plugins-official

# 2단계: 카탈로그 안을 탐색
/plugin marketplace list                  # 등록된 카탈로그 목록
/plugin                                   # GUI: Discover/Installed/Marketplaces/Errors 탭

# 3단계: 골라 설치
/plugin install tdd-suite@claude-plugins-official
```

### 관리 명령어

```bash
/plugin marketplace list                  # 카탈로그 목록
/plugin marketplace update <name>         # 카탈로그 업데이트 (목록 새로고침)
/plugin marketplace remove <name>         # 카탈로그 제거
/plugin list                              # 깔린 플러그인 목록
/plugin uninstall <plugin>@<marketplace>  # 플러그인 제거
```

### 자동 업데이트 정책 (2026-05 기준)

- **공식 마켓플레이스 (Anthropic)**: 자동 업데이트 *기본 ON*
- **서드파티·로컬**: 자동 업데이트 *기본 OFF* — 사용자가 GUI에서 토글
- 전부 끄기: `export DISABLE_AUTOUPDATER=1`
- 자동 업데이트는 *플러그인만* 켜고 Claude Code 본체는 끄기: `export FORCE_AUTOUPDATE_PLUGINS=1` + `DISABLE_AUTOUPDATER=1`

### 팀 공유 — `extraKnownMarketplaces`

`.claude/settings.json` 에 아래를 넣어두면, 팀원이 처음 그 레포에서 Claude Code를 띄울 때 *"이 마켓플레이스를 추가할까요?"* 자동 프롬프트가 뜬다. 사내 사설 카탈로그를 *합의 없이 바로 분배*하는 통로.

```json
{
  "extraKnownMarketplaces": {
    "our-team-tools": {
      "source": {
        "source": "github",
        "repo": "our-org/claude-plugins"
      }
    }
  }
}
```

## 어디서 찾는가 — 2026-05 기준 주요 사이트

### A. Anthropic 공식 카탈로그 (자동 등록됨)

| 카탈로그 | 위치 | 특징 |
|---|---|---|
| `claude-plugins-official` | [github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Anthropic 큐레이션 — 자동 활성화. LSP/통합/워크플로우 100+개 |
| `anthropics/claude-code` | [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) | 공식 데모 플러그인. 시스템 동작 학습용 |

→ 위 두 개는 **`/plugin install <name>@claude-plugins-official`** 로 바로 설치 가능. `/plugin marketplace add` 가 필요 없음.

### B. 공식 웹 브라우저 — 클릭으로 깔 수 있음

- [claude.com/plugins](https://claude.com/plugins) — Anthropic 공식 검색·탐색 페이지. *"Install in Claude Code"* 버튼이 위 명령어를 자동 복사
- [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit) — 자기 플러그인을 공식 카탈로그에 *제출*하는 폼
- [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit) — Console 로그인 사용자용 제출 폼

### C. 커뮤니티 디렉토리 (검색용 메타 사이트)

| 사이트 | 규모 | 결 |
|---|---|---|
| [claudemarketplaces.com](https://claudemarketplaces.com/) | 4,200+ skills · 770+ MCP · 2,500+ marketplaces (2026-05) | 가장 큰 통합 디렉토리. 카탈로그 자체를 *검색* |
| [buildwithclaude.com](https://buildwithclaude.com/) | 큐레이션 카드 형태 | Anthropic 후원, 추천 위주 |
| [aitmpl.com/plugins](https://www.aitmpl.com/plugins/) | 컬렉션 비교 | 큐레이션 + 비교 가이드 |

### D. 큰 커뮤니티 카탈로그 (직접 add 해서 쓰는 결)

| 카탈로그 | 추가 명령어 | 비고 |
|---|---|---|
| `ComposioHQ/awesome-claude-plugins` | `/plugin marketplace add ComposioHQ/awesome-claude-plugins` | 베스트 큐레이션 |
| `jeremylongshore/claude-code-plugins-plus-skills` | 동일 패턴 | **425 plugin · 2,810 skill · 200 agent** — 가장 큰 단일 컬렉션 |
| `wshobson/claude-plugins`, `ananddtyagi/cc-marketplace`, `davila7/...` | 동일 패턴 | 개인 큐레이터 카탈로그들 |

### E. 패키지 매니저 결 — `ccpi`

- [tonsofskills.com](https://tonsofskills.com/) 가 운영하는 **`ccpi` (Claude Code Plugin Installer)** — npm처럼 `ccpi install <name>` 으로 깐다. 카탈로그를 *수동 등록할 필요 없는* 패키지 매니저 스타일.

## Before / After — 발견·설치의 변화

```text
[BEFORE — 2024년 / 마켓플레이스 이전]
1) 구글에 "claude code plugin tdd"
2) GitHub 검색 → 별 수 비교 → README 정독
3) git clone → 폴더 옮기기 → settings.json 수동 수정
4) 재시작 → 동작 확인 → 안 되면 README 다시 정독
→ 첫 플러그인 설치까지 30분~수 시간

[AFTER — 2026-05]
1) /plugin                              ← Discover 탭에서 검색
2) tdd-suite 클릭 → Install
→ 1분 안에 동작 확인
```

## 라이브 시연 가능한 예시

### 시연 1 — 카탈로그 등록부터 설치까지 1분

```bash
[강의 중]
> /plugin marketplace add ComposioHQ/awesome-claude-plugins
✔ Added marketplace 'awesome-claude-plugins' (147 plugins)

> /plugin install commit-helper@awesome-claude-plugins
✔ Installed: skills/commit-helper, hooks/pre-commit.sh

> /commit-helper
[즉시 동작 — 변경사항 분석 후 커밋 메시지 제안]
```
청중에게 *"GitHub 가지 않고 Claude Code 안에서 끝났다"* 가 전달됨.

### 시연 2 — 사내 사설 카탈로그 시뮬레이션

```bash
# 강의용 더미 카탈로그를 로컬에 만들고 즉석 등록
> mkdir -p demo-marketplace/.claude-plugin
> echo '{"name":"demo","plugins":[]}' > demo-marketplace/.claude-plugin/marketplace.json
> /plugin marketplace add ./demo-marketplace
✔ Added local marketplace 'demo'

[청중에게 보여주는 의미]
회사가 *공개 안 된 자기네 플러그인*을 어떻게 분배하는지의 기본형.
사내 GitHub Enterprise 저장소도 같은 명령어로 등록.
```

## 실제 사례 (2026-05 기준)

- **Anthropic 공식 카탈로그**: LSP 11종(Python·TypeScript·Rust·Go·C++·C#·Java·Kotlin·Lua·PHP·Swift) + GitHub/Slack/Figma/Vercel/Sentry 등 외부 통합. **2025년 후반 출시 후 100+개로 성장**.
- **`claude-plugins-official` 자동 활성화**: Claude Code 설치 직후 `/plugin` 만 쳐도 즉시 카탈로그가 보임. *마켓플레이스를 모르는 신규 사용자에게도 닿는다*.
- **`Knowledge Work` 플러그인 14종** (Anthropic, 2025년 말): 영업·법무·HR·마케팅 — *비개발자* 직군 대상. 바이브코딩의 외연 확장 신호.
- **`jeremylongshore/claude-code-plugins-plus-skills`**: 단일 카탈로그 425개 plugin·2,810 skill·200 agent — 큐레이션은 약하지만 *물량* 으로 압도.
- **`tonsofskills.com` + `ccpi`**: 패키지 매니저 결의 등장. *"npm 같은 경험"* 을 명시적 목표로 내건 첫 사례.

## 보안·신뢰 모델 — 반드시 알고 시연할 것

- **플러그인은 사용자 권한으로 *임의 코드 실행* 가능**. 샌드박스 없음.
- Anthropic은 공식 카탈로그(`claude-plugins-official`)만 큐레이션·검토. **서드파티 마켓플레이스의 내용은 검증하지 않음**.
- 조직 단위로 *허용 마켓플레이스 화이트리스트*를 거는 것은 가능 (managed settings).
- **강의 시연 시 권고**: 처음 시연은 공식 카탈로그로. 서드파티 시연은 *코드를 한 번 열어 보여준 뒤* 깔기.

## 강의 연결 포인트

- **플러그인 자체의 정의**는 [Claude Code Plugin](Claude-Code-Plugin.md). 이 문서는 그 *유통·분배 레이어*.
- **Skills/Hooks/MCP/서브에이전트** 각각의 *개별* 설치는 가능하지만, *묶어서 한 번에* 가 마켓플레이스의 핵심 가치. *"풀세팅을 한 줄로"* 의 인프라.
- 사내 도입 논의에서 *"우리 회사 내부 카탈로그 만들 수 있어요?"* 질문이 자주 나옴 → 답: **`extraKnownMarketplaces`** + 사내 GitHub Enterprise 저장소.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code Plugin](Claude-Code-Plugin.md) — *무엇을* 유통하는가 (이 문서는 *어떻게* 유통하는가)
- [Claude Code](Claude-Code.md) — `/plugin` 명령어를 제공하는 호스트
- [Claude Code Skills](Claude-Code-Skills.md) — 마켓플레이스에서 가장 흔히 유통되는 단위
- [Claude Code Hooks](Claude-Code-Hooks.md) — 플러그인이 같이 묶어 들고 오는 자동화 조각
- [MCP](MCP.md) — 플러그인이 같이 묶어 들고 오는 외부 도구 연결
- [oh-my-claudecode](oh-my-claudecode.md) — 마켓플레이스에 올라온 *거대 단일 플러그인*의 사례

## 출처

- [Anthropic — Discover and install prebuilt plugins through marketplaces (Claude Code Docs)](https://code.claude.com/docs/en/discover-plugins) — `/plugin marketplace add` 공식 명세
- [Anthropic — Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) — `marketplace.json` 스키마
- [Anthropic — Plugins reference](https://code.claude.com/docs/en/plugins-reference) — `plugin.json` 매니페스트 + `extraKnownMarketplaces`
- [GitHub: anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — 공식 큐레이션 카탈로그
- [claude.com/plugins](https://claude.com/plugins) — 공식 웹 브라우저
- [claudemarketplaces.com](https://claudemarketplaces.com/) — 가장 큰 통합 디렉토리
- [buildwithclaude.com](https://buildwithclaude.com/) — Anthropic 후원 큐레이션
- [aitmpl.com/plugins](https://www.aitmpl.com/plugins/) — 카탈로그 비교
- [GitHub: ComposioHQ/awesome-claude-plugins](https://github.com/ComposioHQ/awesome-claude-plugins) — 커뮤니티 큐레이션
- [GitHub: jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) — 가장 큰 단일 컬렉션
- [tonsofskills.com](https://tonsofskills.com/) — `ccpi` 패키지 매니저 결
