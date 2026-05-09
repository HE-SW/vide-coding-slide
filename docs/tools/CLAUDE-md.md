# CLAUDE.md — 프로젝트 메모리 파일

> Claude Code가 매 세션 시작마다 자동으로 읽는 **프로젝트 사용설명서**. *"매번 같은 지시를 다시 입력하지 않아도 되게 만드는 한 장의 메모"* — 1강 컨텍스트 엔지니어링의 가장 작은 실전 사례.

## 1. 한 줄 정의

- 프로젝트 루트(또는 `.claude/` 안)에 두는 **마크다운 파일**(`CLAUDE.md`)
- Claude Code가 매번 새 세션을 열 때 **자동으로 컨텍스트에 주입**
- 사용자는 한 번 적어두기만 하면, 같은 지시를 두 번째부터는 입력하지 않아도 됨

## 2. 그전에는 어떤 문제가 있었나

Claude Code 같은 AI 코딩 도구를 쓰다 보면 매 세션 같은 안내를 반복해야 했다:

- "이 프로젝트는 Next.js 14 App Router 써. 페이지는 `app/` 안에 만들고 `pages/`는 쓰지 마."
- "들여쓰기는 스페이스 2칸."
- "테스트는 `npm test` 말고 `pnpm test:unit`로 돌려."
- "이 폴더의 파일은 절대 건드리지 마."

매 세션 첫머리에 사람이 같은 문장을 반복 입력 → **시간 낭비 + 깜빡하면 일관성 깨짐**.

특히 동료와 같은 프로젝트를 작업하면, 사람마다 다르게 안내해 결과물이 어긋나는 문제까지 겹쳤다.

## 3. CLAUDE.md가 어떻게 해결했나

**Anthropic의 공식 메커니즘**: 프로젝트 루트의 `CLAUDE.md`는 Claude가 **세션 시작 시 자동으로 읽고 컨텍스트에 포함**시킨다.

### (1) 위치별로 3계층

| 위치 | 영향 범위 | 용도 |
|---|---|---|
| **프로젝트 루트** `./CLAUDE.md` | 그 프로젝트 전체 | 코딩 컨벤션, 도메인 지식, 명령어 별칭 |
| **사용자 홈** `~/.claude/CLAUDE.md` | 내 모든 프로젝트 | 개인 작업 스타일, 자주 쓰는 톤 |
| **하위 폴더** `./src/feature-x/CLAUDE.md` | 그 폴더 안 작업 | 모듈 단위 특수 규칙 |

→ Claude는 **현재 작업 위치를 기준으로** 가장 가까운 CLAUDE.md부터 거꾸로 거슬러 올라가며 모두 모아 컨텍스트에 넣는다.

### (2) 안에 무엇을 넣나

Anthropic이 권장하는 내용:

- **이 프로젝트가 무엇인가** (한 단락)
- **사용 기술 스택과 규칙** ("Python 3.12 / 들여쓰기 4칸 / 함수에 타입 힌트 필수")
- **프로젝트 구조 요약** (어떤 폴더에 무엇이 있는지)
- **자주 쓰는 명령** (`pnpm dev`, `make test` 등)
- **AI에게 절대 시키면 안 되는 일** ("`production/` 폴더 직접 수정 금지")
- **선호 톤·언어** ("답변은 한국어로", "결과 보고는 짧게")

### (3) 분량과 형식

- **200줄 이내** 권장. 너무 길면 컨텍스트를 잡아먹어 오히려 다른 정보가 밀려난다.
- 마크다운 헤더 + bullet 사용 — Claude가 구조화된 글을 더 잘 따른다.
- 추상적 지침("코드를 깔끔하게 짜")보다 **검증 가능한 구체 지침**("들여쓰기 2칸, 함수당 30줄 이내") 권장.

### (4) 어떻게 만드나

Claude Code 안에서:

- **`/init`** — 현재 프로젝트를 분석해 **CLAUDE.md 초안을 자동 생성**. 비어 있던 프로젝트에서도 한 명령으로 시작 가능.
- **`/memory`** — 기존 CLAUDE.md를 편집기로 열어 수정.
- 또는 그냥 일반 텍스트 편집기로 직접 만들어도 됨.

## 4. 컨텍스트 엔지니어링과의 관계

[컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) 문서에서 정의한 컨텍스트 구성 요소:

> 시스템 지시문 + 사용자 질문 + 검색된 문서 + 도구 출력 + 이전 대화 요약 + ...

CLAUDE.md는 그 중 **시스템 지시문**을 사용자가 직접 작성하는 가장 단순한 형태다. 별도 인프라 없이 **마크다운 파일 한 장**으로 컨텍스트 창의 가장 앞부분을 채워주는 셈.

→ 1강 메시지 *"좋은 답변은 좋은 컨텍스트에서 나온다"* 의 **가장 손에 잡히는 첫 단계**.

## 5. 실전 예시 (강의 데모용)

가장 작은 CLAUDE.md 한 장:

```markdown
# 이 프로젝트

비개발자 대상 강의 슬라이드 자료. 마크다운으로 스크립트 작성, HTML로 슬라이드 렌더링.

## 규칙

- 모든 스크립트는 한국어, 강의톤(~입니다 어미)
- 슬라이드 파일은 `1강/slides/NN-slug.html` 패턴
- 사실은 반드시 출처와 함께 적기

## 자주 쓰는 명령

- 슬라이드 미리보기: `pnpm dev`

## 절대 하지 말 것

- `1강/script.md` 사용자 영역 — AI가 임의 수정 금지
```

(이 레포의 `CLAUDE.md` 자체가 좋은 강의 시연 자료)

## 6. 한계와 주의

- **너무 길면 역효과**: Claude는 [Lost in the Middle](../phenomena/Lost-in-the-Middle.md) 문제로 가운데 정보를 잘 무시한다. 200줄 넘어가면 정작 중요한 규칙이 묻힘.
- **계속 갱신해야 함**: 프로젝트 구조나 규칙이 바뀌면 CLAUDE.md도 손봐야 한다. 안 그러면 *과거 규칙*을 오늘 적용해버림.
- **민감 정보 금지**: API 키·내부 URL·비밀번호 같은 건 절대 넣지 말 것. CLAUDE.md는 보통 git 커밋되어 동료와 공유된다.

## 1강 강의 연결 포인트

- *"지침을 넣어줘야 좋은 답변의 확률이 올라간다"* 메시지의 **가장 단순한 구현체** — 한 장의 파일이면 끝.
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) 슬라이드 직후, [Claude Code](Claude-Code.md) 슬라이드 다음에 자연스럽게 들어감.
- 라이브 데모: 빈 폴더에서 `/init` 한 번 → 자동 생성된 CLAUDE.md를 청중에게 보여주기 → 같은 프롬프트가 CLAUDE.md 유무에 따라 어떻게 달라지는지 비교.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code](Claude-Code.md) — CLAUDE.md를 자동으로 읽는 도구
- [CLI를 쓰는 이유](CLI를-쓰는-이유.md) — CLAUDE.md가 동작하는 무대
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — CLAUDE.md의 상위 개념
- [Lost in the Middle](../phenomena/Lost-in-the-Middle.md) — CLAUDE.md를 너무 길게 쓰면 안 되는 이유
- [andrej-karpathy-skills](andrej-karpathy-skills.md) — 보편 행동 규율 4원칙을 한 장으로 정리한, 가져다 쓸 수 있는 CLAUDE.md 템플릿

## 출처

- [How Claude remembers your project — Claude Code Memory Docs](https://code.claude.com/docs/en/memory) — Anthropic 공식 메모리 문서 (CLAUDE.md 포함)
- [CLAUDE.md Guide: How to Write Context Files — Hannah Stulberg](https://hannahstulberg.substack.com/p/claude-code-for-everything-the-best-personal-assistant-remembers-everything-about-you) — 작성법 실전 가이드
- [CLAUDE.md for .NET Developers — Mukesh Murugan](https://codewithmukesh.com/blog/claude-md-mastery-dotnet/) — 분야별 CLAUDE.md 템플릿
- [Claude Code Memory System Explained — Milvus Blog](https://milvus.io/blog/claude-code-memory-memsearch.md) — 4계층 메모리 구조 분석
- [Inside Claude Code: Architecture — Penligent](https://www.penligent.ai/hackinglabs/inside-claude-code-the-architecture-behind-tools-memory-hooks-and-mcp/) — 메모리·훅·MCP 종합
