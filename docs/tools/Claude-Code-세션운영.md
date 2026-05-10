# Claude Code 세션 운영 — 컨텍스트 오염·세션 분리·메모리 계층

> **2026-05-10 기준, Claude Code 2.x 계열.** 한 세션을 *얼마나 오래·얼마나 깨끗이* 유지하는가가 결과 품질의 80%를 가른다. 같은 모델·같은 프롬프트인데 결과가 *눈에 띄게 나빠지는* 순간이 온다. 정체는 *컨텍스트 오염* — 그리고 그걸 막는 도구가 `/clear`·`/compact`·`/btw`·`/branch`·서브에이전트·CLAUDE.md 계층까지 6가지나 있다.

## 1. 왜 "세션 운영"이 중요해졌나

- LLM은 **컨텍스트 윈도우가 길어질수록 성능이 떨어진다**. 단순히 "더 많은 정보 = 더 좋은 답"이 아니다.
- 2023년 **"Lost in the Middle"** 논문 (Liu et al., Stanford·UC Berkeley) — 컨텍스트 *가운데에 있는 정보*는 모델이 거의 무시한다. 자세히는 [Lost in the Middle](../phenomena/Lost-in-the-Middle.md).
- 게다가 *틀린 정보가 한번 컨텍스트에 박히면* — 후속 응답에서 모델이 그 틀린 정보를 *근거로* 삼는다. 이게 **컨텍스트 오염 (Context Pollution)**.
- → *"한 세션에 다 쌓아놓으면 똑똑해진다"* 는 직관은 **거짓**. 세션을 *주기적으로 끊고 정리*하는 운영 기술이 필요해졌다.

## 2. 그전에는 어떤 문제가 있었나 — *한 세션에 다 쌓는 결*

2023년 ChatGPT 초기엔 *컨텍스트 오염*이라는 단어 자체가 거의 안 쓰였다. 사용자는 *대화가 길어질수록 AI가 멍청해지는 것* 을 체감했지만, *왜* 그런지·*어떻게* 풀 지 답이 없었다.

- 모델이 헛소리하면 → 그냥 새 채팅 열기 (지금까지 쌓은 컨텍스트도 같이 사라짐)
- 부분만 살리고 싶어도 도구가 없음

**일상 비유**: 책상 한 장에 모든 메모를 다 쌓아놓고 *"필요한 것만 골라봐"* 하는 것과 같다. 책상 위가 깨끗할 때는 한눈에 보이는데, 한 시간 일하고 나면 *어디에 뭐 있었는지 본인도 모르는 상태*. 책상을 *주기적으로 치우는 습관*이 없으면 결국 종이 하나 찾는 데 5분 걸리게 된다. **컨텍스트도 책상이다**.

## 3. 어떻게 해결했나 — 6가지 도구

---

## A. 컨텍스트 오염 — 4가지 명령어, 결이 다 다르다

| 명령 | 한 줄 정의 | 언제 쓰나 | 보존되는 것 |
|---|---|---|---|
| **`/clear`** | 대화 *완전 초기화*. 새 세션. | 작업 주제가 *완전히 바뀔 때* | CLAUDE.md, auto memory만 유지 |
| **`/compact [지시]`** | 지금까지 대화를 *요약*해서 토큰 회수 | 같은 작업 계속 가는데 *토큰이 빠듯할 때* | 요약 + CLAUDE.md (재로드됨) |
| **`/btw`** | *곁질문*. 메인 흐름 안 건드리고 잠깐 다른 거 묻기 | 작업 중 *잠깐 모르는 용어* 떠올라서 물어볼 때 | 메인 컨텍스트 그대로, 답은 히스토리에 안 남음 |
| **`/branch`** | 현재 세션을 *복사*해서 새 ID로 갈래치기 | *위험한 시도*를 메인 흐름에 영향 없이 해보고 싶을 때 | 양쪽 다 — 원본은 그대로 |

### `/clear` vs `/compact` — 가장 자주 헷갈리는 짝

```text
[/clear]
대화 → 통째로 삭제
프로젝트 메모리 (CLAUDE.md) → 유지
→ "방금 한 시간 작업한 기억은 다 사라진다. 책상을 통째로 비운 상태"

[/compact]
대화 → "X 작업했고, 결론은 Y였음" 같은 요약 한 줄로 줄임
프로젝트 메모리 (CLAUDE.md) → 다시 로드됨 (compact 직후엔 항상 깨끗한 가이드라인 위에서 시작)
→ "방금 한 시간을 한 줄로 압축했지만 그 결론은 살아있음"
```

`/compact API 변경 부분만 남겨줘` 처럼 **초점을 지정**할 수 있다. 무차별 요약보다 훨씬 깨끗.

> ⚠️ `/compact` 직후엔 *세부 지침*이 휘발될 가능성. 요약 후 *"잊지 말 것: …"* 한 줄로 핵심 제약을 다시 박아두는 습관 권장.

### `/btw` — 곁질문 (가장 저평가된 도구)

```bash
[메인 작업 진행 중]
> @src/payment.ts 에 멱등성(idempotency) 키 추가 중...

[잠깐 헷갈림]
> /btw 멱등성 키랑 트랜잭션 ID 차이가 뭐였지?
[Claude가 답변 — 도구 사용 없음, 읽기 전용, 답은 히스토리에 안 남음]

[메인 작업으로 복귀]
> 좋아 멱등성 키로 그대로 가자. 헤더 이름은 X-Idempotency-Key.
```

핵심: **메인 컨텍스트는 그대로**, 곁질문은 *프롬프트 캐시 재사용*으로 저비용. 곁질문의 답이 *메인 흐름을 오염시키지 않는다*. 강의에서 시연하면 *"AI한테도 잠깐 다른 질문 가능하구나"* 가 새롭게 와닿음.

### `/branch` — 위험한 시도용 갈래

```bash
[메인 세션에서]
> @src/db.ts 에 새 인덱스 추가하는 마이그레이션 만들어줘
[Claude가 진행 중]

> /branch
[현재 세션 복사 → 새 세션 ID로 분기]

[브랜치 세션에서 — 위험한 실험]
> 이 마이그레이션을 실제 prod DB에 미리 dry-run 해볼래?
[혹시 망쳐도 메인 흐름은 안전]

[/resume → 메인 세션 선택 → 원래 흐름 그대로 이어감]
```

`/branch`는 git의 branch와 같은 개념을 *대화 세션*에 적용한 것. 양쪽 다 살아있음.

### `/rewind` (=ESC 두 번) — 시간 되돌리기

작업이 *잘못된 방향*으로 갔을 때, 특정 메시지까지 거슬러 올라가면서 **그 이후의 코드 변경까지 함께 되돌린다**. *"AI가 망친 걸 한 줄로 복구"*. ESC 두 번 빠르게가 가장 빠른 호출법. 자세히는 [Claude Code 입력 문법](Claude-Code-입력문법.md).

---

## B. 세션 분리 — *큰 작업을 작은 세션 여럿*으로

한 세션 안에 *모든 일을 다 시키지 말라*. 컨텍스트가 길어지면 오염도 커지고 *Lost-in-the-Middle*도 발동한다. 분리 도구 4가지:

### 1. 서브에이전트(Subagent) 위임 — 가장 강력한 격리

`Agent` 도구 / `/agents` 슬래시 — *전문 분야의 작은 AI 동료*에게 일을 떼어줌.

핵심 메커니즘:
```text
메인 세션  ──[질문/지시]──>  서브에이전트
메인 세션  <──[요약 답만]──  서브에이전트
                            ↑ 서브에이전트의 *내부 대화* 는 메인에 안 들어옴
```

→ **메인 컨텍스트는 *깨끗한 답만* 받는다**. 100파일 검색 → 답 1줄. 작업당 *수만 토큰의 오염*을 격리. 자세히는 [서브에이전트](서브에이전트.md).

### 2. `/branch` — 같은 출발점에서 갈래

위 A섹션 참고. *"여기까지는 같이, 이후는 따로"* 패턴.

### 3. git worktree + 다중 Claude Code 인스턴스

진짜 큰 분리는 *세션이 아니라 작업 트리* 단위로 가른다.

```bash
# 메인 worktree
$ git worktree add ../project-feature-A feature-A
$ cd ../project-feature-A && claude

# 다른 worktree에서 평행 진행
$ git worktree add ../project-feature-B feature-B
$ cd ../project-feature-B && claude
```

각 인스턴스는 *완전히 독립*된 컨텍스트·도구 상태·CLAUDE.md 로드. *같은 프로젝트의 다른 측면을 동시에* 진행할 때 표준 패턴.

> 💡 모든 worktree는 *같은 프로젝트 메모리* 를 공유한다. 즉 한 worktree에서 학습한 것이 다른 worktree에서도 살아있음.

### 4. 헤드리스 모드 (`claude -p`) — *세션 자체가 1회용*

```bash
$ echo "@src/users.ts 의 함수 목록만 뽑아줘" | claude -p
```

자동화·CI·스크립트용. **호출이 끝나면 컨텍스트가 사라진다** — 영속적 오염이 원천 차단. 자세히는 [Claude Code 헤드리스 모드](Claude-Code-Headless-모드.md).

---

## C. CLAUDE.md 계층과 `@path` import — *지속적인 컨텍스트* 의 위생

매 세션마다 다시 박아넣을 필요 없는 *영속 컨텍스트*는 CLAUDE.md에 둔다. 4계층으로 나뉨:

| 계층 | 위치 | 범위 | 공유 |
|---|---|---|---|
| **Managed** | `/Library/Application Support/ClaudeCode/CLAUDE.md` (mac) `/etc/claude-code/CLAUDE.md` (Linux) | 조직 전체 — IT가 배포 | 회사 모든 사용자 |
| **Project** | `./CLAUDE.md` 또는 `./.claude/CLAUDE.md` | 팀 (git 커밋) | 동료 전체 |
| **User** | `~/.claude/CLAUDE.md` | 본인 (모든 프로젝트) | 본인만 |
| **Local** | `./CLAUDE.local.md` | 본인 (현재 프로젝트) | 본인만, `.gitignore` 필수 |

**로드 순서**: 파일 시스템 루트→작업 디렉토리로 내려오면서 발견된 모든 CLAUDE.md를 연결. 각 레벨에서 `CLAUDE.md` → `CLAUDE.local.md` 순.

### `@path` import — CLAUDE.md 안에서 다른 마크다운 끌어오기

```markdown
# Project CLAUDE.md
프로젝트 개요는 @README.md 참조.
API 규약은 @docs/api-guide.md.
공통 코딩 규율은 @~/.claude/shared-coding-rules.md.
```

- 상대 경로: *그 파일 기준* (작업 디렉토리 기준 아님)
- 절대 경로 + `~/`: 사용자 홈 기준
- **재귀 import 깊이 제한 5단계**

→ CLAUDE.md를 *얇게* 두고 큰 가이드는 별도 파일로 빠지게 하는 패턴이 표준. 자세히는 [CLAUDE.md](CLAUDE-md.md), [문서 주도 개발](../techniques/문서-주도-개발.md).

---

## D. 컨텍스트 모니터링 — `/context`

```bash
> /context
[현재 컨텍스트 사용량을 색깔 격자로 시각화]
██████████░░░░░░  60% used (120K / 200K tokens)
```

**경험칙**: 60% 넘어가면 슬슬 `/compact` 고려, 80% 넘으면 즉시. *Lost-in-the-Middle*은 컨텍스트가 길수록 강해진다.

`/usage` (=`/cost`)로 비용·턴수도 같이 본다. 한 작업이 *비정상적으로 비싸지면* 보통 컨텍스트 오염이 원인.

---

## 실전 운영 — 작업 결별 권장 흐름

```text
[작은 작업 — 한 가지 기능 추가]
→ 그냥 한 세션에서 끝까지

[중간 작업 — 한 개 모듈 리팩토링]
→ /context 자주 보기
→ 60% 넘으면 /compact "지금까지 결정 + 남은 할일만"
→ 끝나면 /clear

[큰 작업 — 새 기능 + 버그 수정 + 테스트]
→ 새 기능: 메인 세션
→ 버그 수정: /branch 분기 (또는 worktree)
→ 테스트: 서브에이전트 위임
→ 잠깐 모르는 거: /btw 곁질문
→ 모듈 끝나면 /clear → 다음 모듈
```

## Before / After — 운영의 차이

```text
[BEFORE — 한 세션 끝까지 끌고 가기]
1) "users 모듈 만들어줘"
2) "이제 payments도"
3) "저번에 만든 users는 이렇게 고쳐주고..."
4) [1시간 후] AI가 헛소리 시작 — 자기가 만든 함수 이름도 잊어버림
5) /clear → 모든 컨텍스트 잃음 → 처음부터

[AFTER — 분리 운영]
1) "users 모듈 만들어줘" → 끝나면 /clear
2) (CLAUDE.md엔 "users 모듈은 src/users 에 만들었다" 한 줄 메모)
3) "payments 모듈 만들어줘" → 깨끗한 컨텍스트에서 시작
4) "users 수정" 필요 시 → @src/users.ts mention → 정확한 위치만 컨텍스트에 들어옴
```

## 라이브 시연 가능한 예시

### 시연 1 — `/context` 시각화 + `/compact`

```bash
[작업 30분 후]
> /context
██████████████░░ 75%

> /compact 지금까지 만든 함수 목록과 다음 할일만 남겨줘
[요약 → 200토큰 한 줄로 압축]

> /context
██░░░░░░░░░░░░░░ 12%
```
*"AI도 책상 정리가 필요하다"* — 청중에게 가장 강하게 박히는 메시지.

### 시연 2 — 서브에이전트 격리

```bash
> 메인 세션 컨텍스트: ████████░░ 50%
> 100개 파일에서 deprecated API 호출 다 찾아줘 (Agent 도구 위임)
[서브에이전트가 100파일 읽고 수만 토큰 처리]
[메인엔 "37개 발견, 위치 목록 첨부" 답만 들어옴]

> 메인 세션 컨텍스트: ████████░░ 51% (단 1% 증가)
```
서브에이전트의 *오염 격리* 효과를 수치로 보여주면 강력함.

## 강의 연결 포인트

- **Lost-in-the-Middle 슬라이드**와 직접 연결. *"왜 세션 운영을 해야 하나"* 의 근거.
- **하니스 엔지니어링** — 세션 운영은 하니스의 *Control & State* 레이어. 자세히는 [Control & State](../techniques/harness/control-and-state.md).
- **비용·효율** — `/context` 모니터링 + `/compact` + 서브에이전트 = 가장 큰 토큰 절감 트리오.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code 입력 문법](Claude-Code-입력문법.md) — `!`/`@` 으로 *컨텍스트에 박을 정보의 양*을 정밀 조절. 짝 문서.
- [Claude Code](Claude-Code.md) — 슬래시 명령어 전체 표
- [CLAUDE.md](CLAUDE-md.md) — 4계층 메모리 deep dive
- [Lost in the Middle](../phenomena/Lost-in-the-Middle.md) — 왜 컨텍스트가 길어지면 안 좋은가
- [환각](../phenomena/환각.md) — 오염된 컨텍스트가 헛소리의 흔한 원인
- [서브에이전트](서브에이전트.md) — 가장 강력한 컨텍스트 격리 도구
- [Claude Code 헤드리스 모드](Claude-Code-Headless-모드.md) — 1회용 세션 = 영속 오염 차단
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — 이 문서의 *이론적 토대*
- [Control & State (하니스)](../techniques/harness/control-and-state.md) — Phase 분할·docs 영속화의 더 큰 그림
- [문서 주도 개발](../techniques/문서-주도-개발.md) — 영속 컨텍스트의 4종 문서 패턴

## 출처

- [Claude Code Memory & CLAUDE.md (Claude Code Docs)](https://code.claude.com/docs/en/memory) — 4계층 메모리·`@path` import 공식 명세
- [Claude Code Commands Reference](https://code.claude.com/docs/en/commands) — `/clear`·`/compact`·`/btw`·`/branch`·`/rewind` 동작
- [Claude Code Cheatsheet (Anthropic Support)](https://support.claude.com/en/articles/14553413-claude-code-cheatsheet) — 운영 단축키 통합
- [Liu et al. 2023 — Lost in the Middle](https://arxiv.org/abs/2307.03172) — 컨텍스트 위치 편향 원논문
- 본 문서 작성 시점에 Claude Code 내장 가이드 에이전트(`claude-code-guide`)로 직접 교차 검증 (2026-05-10).
