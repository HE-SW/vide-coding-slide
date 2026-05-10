# Claude Code Skills (스킬)

> 자주 쓰는 작업 절차에 *이름표를 붙여둔* 마크다운 파일. **`/이름`** 한 줄로 호출. Skills 도입 슬라이드의 정확한 본문이며, 후속 강의에서 다루는 `/harness`·`/review` 도 모두 Skills.

## 1. 왜 "Skill"이라고 부르나

- 영어 그대로 *"기술·솜씨"*. 자주 반복하는 *작업의 묶음*에 이름을 붙인다는 뜻.
- **Anthropic 공식 도입**: Claude Code의 첫 출시(2025-02) 이후 점진적으로 추가. 2026년 현재 *Skills + Plugins* 가 Claude Code 확장의 양대 축.
- **OpenCode·Cursor·Gemini CLI** 등 다른 코딩 에이전트도 비슷한 *Skills* 개념을 도입 — 사실상 멀티 에이전트 도구 사이의 *공용 어휘*가 되는 중.

## 2. 그전에는 어떤 문제가 있었나

같은 작업을 매번 길게 시켜야 했다.

- *"현재 디렉토리의 README를 읽고, 강의톤으로 슬라이드 5장 만들어주고, slides/ 폴더에 NN-제목.html 형식으로 저장해줘"* 를 매번 반복
- 동료에게 *"이 작업 너도 자주 하지? 어떤 프롬프트로?"* — 사람마다 다르게 시키니 결과도 제각각
- 잘 작동하는 프롬프트 *발견* 후에도 — *재사용 단위*가 없어 한 사람 머리에만 남음

**일상 비유**: 회사에서 자주 쓰는 보고서 양식이 *워드 파일*에 박혀 있어, 매번 새 문서를 빈 채로 시작하는 것. Skills는 그 양식을 *템플릿 라이브러리*로 분리해 슬래시 한 번에 불러오는 것.

## 3. 어떻게 해결했나 — SKILL.md 한 장

Skills는 `.claude/skills/` 또는 `~/.claude/skills/` 폴더 아래에 *마크다운 파일 한 장*으로 정의된다.

### 디렉토리 구조

```text
~/.claude/skills/                    개인 라이브러리 (모든 프로젝트)
└── presentation_script/
    ├── SKILL.md                     ← 핵심: frontmatter + 지시문
    ├── scripts/                     선택: 스킬이 호출하는 보조 스크립트
    │   └── slides_renderer.py
    ├── references/                  선택: 모델이 참조할 자료
    │   └── style_guide.md
    └── assets/                      선택: 정적 자산 (이미지·CSS 등)

.claude/skills/                       프로젝트 라이브러리 (이 레포 전용, git 커밋)
└── harness/
    └── SKILL.md
```

### SKILL.md — YAML Frontmatter

```markdown
---
name: presentation_script
description: |
  YouTube 영상 발표용 script.md 자동 정돈/작성. 사용자가 raw하게 작성한 대본
  초안을 받아서, presentation_slides 스킬이 잘 받아먹는 구조로 변환한다.
  '대본 작성', '발표 대본 정리' 등의 요청에 트리거.
triggers:
  - "대본 정리"
  - "presentation script"
  - "/presentation_script"
permissions:
  tools: [Read, Edit, Write]
---

# 발표 대본 정돈 스킬

## 절차
1. 입력 받은 마크다운을 읽는다
2. 섹션 단위로 분리: 인트로 / 본문 / 마무리
3. 각 섹션을 강의톤(~입니다)으로 변환
4. 출력은 `script.md` 한 장으로 저장
```

**핵심 필드**:
- `name`: 호출용 이름 (`/presentation_script` 또는 자연어 트리거)
- `description`: Claude가 *언제 이 스킬을 쓸지* 판단하는 단서. 길게 쓸수록 정확
- `triggers`: 자연어 음성·STT 별칭 (선택)
- `permissions`: 이 스킬이 쓸 수 있는 도구 화이트리스트 (선택)

## 두 저장 위치

| 위치 | 범위 | 용도 |
|---|---|---|
| `~/.claude/skills/` | 내 모든 프로젝트 | *발표 대본 정리* 같은 범용 작업 |
| `.claude/skills/` | 이 레포 전용 (git 공유) | `/harness`, `/review` 같은 *프로젝트 특화* 절차 |

→ 같은 이름의 스킬이 두 곳 모두에 있으면 **프로젝트 스킬이 우선**.

## Before / After

```text
[BEFORE — 매번 길게 시키기]
USER: "이 마크다운을 읽고 강의톤으로 정돈해줘. 인트로/본문/마무리로
       나누고, ~입니다 어미로 통일해줘. 출력은 script.md 로..."
       (200자 프롬프트, 매번 반복)

[AFTER — Skill 등록 후]
USER: "/presentation_script"
       또는 "대본 정리해줘"
       → 같은 작업이 한 줄로 시작됨
```

## 라이브 시연 가능한 예시 — 이 강의 레포

이 강의 레포의 `.claude/skills/` 에는 두 개의 스킬이 있다 (Skills 도입 슬라이드 본문):

```text
.claude/skills/
├── presentation_script/   →  /presentation_script  대본 정돈
└── presentation_slides/   →  /presentation_slides  HTML 슬라이드 생성
```

여러분이 보고 있는 이 슬라이드 자체가 — `/presentation_slides` 한 줄로 만들어진 결과물이다.

## 실제 사례 (2026 기준)

- **Anthropic 공식 마켓플레이스** `claude-plugins-official`: 2026-03 기준 101개 plugin 내장. 각 plugin은 1개 이상의 skill을 묶음.
- **커뮤니티 마켓플레이스**:
  - `alirezarezvani/claude-skills`: **232개+ 스킬** (엔지니어링·마케팅·법무·임원 자문)
  - `jeremylongshore/claude-code-plugins-plus-skills`: **425 plugin · 2,810 skill · 200 agent**
  - `travisvn/awesome-claude-skills`: 큐레이션 리스트
- **2026년 트렌드**: skill의 *공통 표준화* 진행 중 — OpenCode·Gemini CLI 등이 `SKILL.md` 호환 형식 채택.

## Skills vs Subagents vs Hooks vs Plugins — 헷갈리지 마세요

| | Skills | Subagents | Hooks | Plugins |
|---|---|---|---|---|
| 호출 | `/이름` 슬래시 | 메인이 자동 위임 | 이벤트 발생 시 자동 | 묶음 단위 설치 |
| 실행 시점 | 사용자가 부를 때 | 작업 위임 시 | 매 이벤트마다 | (skills+hooks+MCP 묶음) |
| 비용 | 호출당 | 호출당 | 매번 | 묶음 |
| 강의 도입 위치 | Skills 도입 슬라이드 (`/harness` 활용) | 확장 도입 슬라이드 | Hooks 도입 슬라이드 | 별도 doc |

각 개념은 *겹치지 않고* — *다른 추상화 층*이다.

## 강의 연결 포인트

- **Skills 도입 슬라이드** [데모: 22-skills.html] — 정확히 이 문서의 본문. *"이 슬라이드 자체가 `/presentation_slides` 로 만들어진 것"* 메시지.
- **`/harness`·`/review` 슬라이드** [데모: 10-skills.html] — 두 스킬이 *어떻게 한 줄 호출이 되는가* 의 detail.
- **`/harness` 5단계 흐름 슬라이드** [데모: 11-harness-flow.html] — `/harness` 가 실제로 작동할 때의 흐름.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code](Claude-Code.md) — Skills 호스트
- [Claude Code 플러그인](Claude-Code-Plugin.md) — Skill 여러 개를 묶는 상위 개념
- [Plugin Marketplace](Plugin-Marketplace.md) — Skill을 묶은 플러그인이 *유통되는* 카탈로그 레이어
- [Claude Code Hooks](Claude-Code-Hooks.md) — *자동 실행* 측 (Skill = 사용자 호출, Hook = 이벤트 발화)
- [서브에이전트](서브에이전트.md) — *분업* 측 (Skill = 절차, Subagent = 일꾼)
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — Skill의 본문이 *재사용 컨텍스트*

## 출처

- [Anthropic — Extend Claude with skills (Claude Code Docs)](https://code.claude.com/docs/en/skills) — 공식 명세
- [BrightCoding: Claude Skills Marketplace (2026-04)](https://www.blog.brightcoding.dev/2026/04/26/claude-skills-marketplace-the-essential-plugin-hub-for-developers) — 마켓플레이스 종합
- [Firecrawl: Best Claude Code Skills to Try in 2026](https://www.firecrawl.dev/blog/best-claude-code-skills) — 큐레이션
- [GitHub: alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — 232+ 스킬 컬렉션
- [GitHub: travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) — awesome list
- [Where Are Claude Skills Stored? (Agensi)](https://www.agensi.io/learn/where-are-claude-skills-stored) — 경로 설명
