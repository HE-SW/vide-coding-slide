# 2강 — Claude Code를 직접 마스터한다 (v2)

비개발자 대상 강의. 1강 v2(워크숍)를 수강한 청중 + Claude Code 설치 완료 + 1강 v2 직후 진행.

> 작성 규칙
>
> - `[데모: NN-xxx.html]` — 슬라이드 전환 큐 (slides/ 안 파일명과 1:1 매핑)
> - `[함께 입력 #N]` — 청중이 자기 PC에 동시 입력 (3회)
> - "회수 → 1강 슬롯 NN" 같은 메모는 _발표자 노트_. 슬라이드 본문엔 노출 X (1강 v2 P1 원칙)
> - 시점 의존 단어("최근"·"요즘"·"올해") 금지 — 절대 날짜로 (오늘 = 2026-05-11)
> - Claude Code 버전 기준 = **v2.1.x** / 모델 Opus 4.7 · Sonnet 4.6 · Haiku 4.5

## 0부 — 도입 

### 01 표지

오늘 — *어제 가르친 그 도구를 직접 마스터*하는 시간.

```text
VIBE CODING · 2강 (v2)

Claude Code를 직접 마스터한다

 · 강의 + 라이브 3회 · v2.1.x 기준
```

[데모: 01-cover.html]

---

### 02 1강 회수 — 동심원 한 장

어제(혹은 1주 전) 본 그림 다시 한 번.

```text
 ┌──────────────────────────────┐
 │ 하니스 (모델 주변 환경 전체) │
 │ ┌────────────────────────┐ │
 │ │ 컨텍스트 (5요소) │ │
 │ │ ┌──────────────────┐ │ │
 │ │ │ 프롬프트 (4기법) │ │ │
 │ │ └──────────────────┘ │ │
 │ └────────────────────────┘ │
 └──────────────────────────────┘
```

세 단어 — _프롬프트 ⊂ 컨텍스트 ⊂ 하니스_. 1강은 *이 셋이 무엇이고 왜 동시에 박혀야 하는지*까지 봤어요. 오늘은 그 셋이 _살아있는 도구_ — **Claude Code 자체**를 직접 마스터합니다.

[데모: 02-recap-circles.html]

---

### 03 오늘의 흐름

1강 마지막에서 _"동심원·5요소·하니스 4축이 모두 이 한 도구 안에 박혀있다"_ 했죠. 오늘은 그 *박혀있는 4가지*를 하나씩 손에 잡히게 풉니다.

```text
1부 기본기 Plan Mode · 모드 4종 · CLAUDE.md
2부 실전 사용 컨텍스트 관리 · 워크플로우 · TDD · docs 운영
3부 자동화 4부품 Skills · Sub-Agent · Hooks · MCP
4부 마무리 압축 + 3강 예고
```

[함께 입력]은 3번 — 비개발자도 무리 없이 따라치는 _짧은 명령_ 위주예요. 시작합시다.

[데모: 03-promise.html]

---

## 1부 — Claude Code 기본기 

### 04 CLAUDE.md — 5단계 계층

1강에서 *팀 룰북*이라고 봤죠. 그게 *한 장*이 아니라 — **5단계 계층**입니다.

```text
Enterprise 조직 정책 회사 사훈 — 사용자가 끌 수 없음
~/.claude/ User (글로벌) 내 모든 프로젝트 공통 (한국어 답변 등)
프로젝트 루트 Project 팀 위키 — 레포에 커밋
CLAUDE.local Local 내 책상 메모 — .gitignore
서브폴더 Subdirectory 해당 폴더 작업 시에만 자동 로드
```

→ 위에서 아래로 갈수록 _더 구체적_. **더 구체적인 쪽이 우선되도록 설계**됨.

_단, CLAUDE.md는 "강제 설정"이 아니라 "컨텍스트"라서_ — 충돌 규칙은 _항상 100% 일관되게_ 따르진 않을 수 있어요. 정말 어겨선 안 되는 규칙은 다음 슬라이드의 **CRITICAL 패턴**으로 강도를 키워야 합니다.

[데모: 04-claude-md-hierarchy.html]

---

### 05 CLAUDE.md — @import으로 분리

200줄 한계 때문에 — _모든 내용을 직접 적으면_ 컨텍스트 잡아먹어요. 해법: **CLAUDE.md엔 참조만, 본문은 별도 파일로 분리**.

```text
[Before — 모든 내용 직접]
# CLAUDE.md (나쁜 예)
## API 엔드포인트
- POST /api/auth/login - 로그인...
- POST /api/auth/register - 회원가입...
- ... (50개 더)
- (200줄 훌쩍 넘김)

[After — 참조만]
# CLAUDE.md (좋은 예)
## 프로젝트 문서
- API 스펙: @docs/api-spec.md
- DB 스키마: @docs/db-schema.md
- 인증 설계: @docs/auth.md
- 코딩 컨벤션: @docs/conventions.md

→ @import는 *세션 시작 시* 최대 5단계 재귀로 *전부* 컨텍스트에 로드됨
→ "필요할 때만" 읽히는 게 아니라 *한 번에* 통째로 들어옴
```

**중요한 진실** — @import는 _lazy load 아님_. 시작할 때 5단계 재귀로 _모두 불러온다_. 그래서 *200줄 룰이 더 중요*합니다. 분리는 *작성·관리 편의*용이지 *토큰 절약*은 아님.

**진짜 lazy load는 따로 있어요** — _Subdirectory CLAUDE.md_(해당 폴더 작업 시에만 자동 로드)와 _Skills_(호출 시에만 본문 로드). 이 둘은 docs 폴더 운영과 Skills 구조 슬라이드에서 다시.

[데모: 05-claude-md-import.html]

---

### 06 라이브 — `/init`으로 CLAUDE.md 만들기

이론은 충분. 직접 만들어봅니다.

```text
[함께 입력 #1 — 모두 자기 폴더에서]

> /init
```

- 진행자 화면: 빈 폴더 또는 기존 프로젝트에서 `/init` 실행
- 청중: 자기 PC에서 동시 입력
- 결과 비교 — 폴더 구조에 따라 _다르게 자동 생성_

청중 폴더가 _비어있으면_ — 강사 화면 공유로 대신.

**관찰 포인트** _(강사가 청중에게 던질 질문)_:

- Claude가 *어떤 항목*들을 잡았나? (기술 스택? 폴더 구조?)
- _내가 직접 적으면 빼먹었을_ 항목이 있나?
- 200줄 넘었나? → 넘으면 `@import`로 분리

[데모: 06-init-live.html]

---

### 07 200줄 룰 + CRITICAL 패턴

CLAUDE.md 작성 모범 사례 — 두 가지만:

**① 200줄 이하 유지** — 길어지면 컨텍스트 소모 ↑, Claude가 규칙을 _일관되게 못 따름_.

**② CRITICAL 접두어** — _절대 위반 금지_ 표시.

```markdown
## 아키텍처 규칙

- CRITICAL: 모든 API 로직은 app/api/ 라우트 핸들러에서만 처리
- CRITICAL: secrets는 .env에만 — 코드에 하드코딩 절대 금지

## 개발 프로세스

- IMPORTANT: 새 기능은 테스트 먼저 작성 (TDD)
```

**왜 통하나** — 모델은 *영어 대문자*를 *강조 신호*로 가중치 더 둠. Anthropic 공식 가이드도 `CRITICAL`·`IMPORTANT`·`NEVER`·`ALWAYS`를 *지시문 강도 표시*로 권장.

**팁** — bullet *맨 앞*에 둬야 *전체 항목 라벨*로 읽힘. 중간에 들어가면 *조건절*로 약하게 해석됨.

[데모: 07-critical-pattern.html]

---

### 08 Plan Mode — 도면 먼저

CLAUDE.md로 *프로젝트 룰북*은 박았어요. 이제 그 룰북 위에서 _실제로 일을 시작하는 모드_ 차례.

**일상 비유** — 집 짓기. 망치를 들고 _바로 못부터 박기 vs 도면을 그리고 시작_. AI가 *코드 바로 쓰기 vs 계획 먼저*도 똑같아요.

**Before / After**:

```text
[Before] > "사용자 인증 기능 만들어줘"
 → AI가 갑자기 8개 파일 만지기 시작
 → 3번째 파일에서 방향 어긋남
 → 처음부터 다시 시키기 (토큰·시간 낭비)

[After] > /plan 사용자 인증 기능 만들어줘
 → AI: *계획만 제시*
 1. DB 스키마 변경
 2. API 엔드포인트 3개
 3. 프론트 페이지 1개
 4. 각 단계마다 테스트
 → 청중이 *읽고 수정*
 → 만족하면 Auto-Accept로 전환해서 실행
```

**Anthropic 공식 4단계** — _Explore → Plan → Code → Verify_. Plan Mode는 이 흐름의 2번 칸을 _공식 모드로_ 박아둔 것.

**라이브 시연** — 강사가 `Shift+Tab` 두 번 → Plan Mode 진입 → 같이 짠 작업 한 줄 → 계획 노출. *코드 한 줄도 안 쓰는 모드*가 어떻게 일을 시작하는지 청중이 직접 봄.

[데모: 08-plan-mode.html]

---

### 09 모드 4종 — 언제 어느 모드

`Shift + Tab`을 누르면 모드가 순환해요. 4개를 한 장에 (괄호 안은 _실제 이름_ — 청중이 설정 파일에서 보게 될 표기):

```text
┌──────────────────────────────┬────────────────────────────────┐
│ Normal (default) │ 매 작업 전 묻기 (기본값) │
│ Auto-Accept (acceptEdits) ⏵⏵ │ 파일 편집 + 안전한 bash 자동 │
│ Plan (plan) ⏸ │ 읽기 전용, 계획만 세움 │
│ Auto (auto) │ AI 분류기가 매 호출 안전성 판단 │
└──────────────────────────────┴────────────────────────────────┘
```

**Auto Mode 사용 조건** _(중요 — 일부 청중은 화면에 안 보일 수 있음)_:

- 플랜: **Max / Team / Enterprise / API** — _Pro 불가_
- 모델: Sonnet 4.6 · Opus 4.6 · Opus 4.7
- Provider: Anthropic API 전용 (Bedrock/Vertex 불가)
- 버전: v2.1.83+

→ 화면에 Auto가 안 나오면 _"내 플랜에선 못 쓰는구나"_ 라고 안내. _Pro 플랜 청중은 일반 3모드만_.

**Auto Mode가 차단한 한 사례** — 이 레포 작업 중 _"git push origin main"_ 시도 → 분류기가 _"기본 브랜치 보호"_ 사유로 차단. 사용자가 따로 명시한 후 통과. 청중이 *"AI가 내 명령을 거절할 수도 있다"*는 걸 처음 보는 순간.

**언제 어느 모드** — 새 작업은 항상 _Plan Mode_, 검토 후 *Auto-Accept*로 전환. 위험한 작업(K8s·배포·결제)은 _Normal(default)로 회귀_.

[데모: 09-four-modes.html]

---

### 10 1부 정리 — 세 줄

```text
한 모드 Plan Mode (Shift+Tab × 2 / /plan)
한 파일 CLAUDE.md (200줄, CRITICAL, @import)
한 안전망 /sandbox · /permissions · /rewind
```

이 세 줄이 _Claude Code 기본기의 핵심_. 더 깊이는 docs/tools/Claude-Code-퍼미션모드.md · CLAUDE-md.md 참조.

[데모: 10-part1-summary.html]

---

## 2부 — 실전 사용법 

### 11 2부 표지

```text
PART 2 · 

실전 사용법

청중이 가장 자주 막히는 영역
한 세션 = 한 피처 · 컨텍스트 4도구 · Plan-Code-Verify · TDD · docs 운영
```

[데모: 11-part2-cover.html]

---

### 12 한 세션 = 한 피처

1강에서 본 **Lost in the Middle** 기억나시죠. 컨텍스트가 길어질수록 _가운데가 흐려진다_. 그 현상을 *운영 원칙*으로 박은 한 줄:

```text
한 세션 = 한 피처
```

**왜** — 여러 기능을 한 세션에서 연달아 하면:

- 컨텍스트 누적 → 가운데 흐려짐 (Lost in the Middle)
- 이전 작업의 *임시 가설*이 다음 작업에 새어 들어옴 (오염)
- 80% 넘기면 응답 품질 _눈에 띄게_ 떨어짐

**실전 워크플로우**:

1. Plan Mode에서 전체 작업을 설계
2. 첫 단계만 구현 → 완료
3. `/clear` 또는 새 세션
4. 다음 단계로

_"신선한 컨텍스트가 부풀어진 컨텍스트보다 항상 낫다."_

[데모: 12-one-session-one-feature.html]

---

### 13 컨텍스트 관리 4도구

세션 운영의 칼 — 4개만 외우면 됨.

```text
/context 토큰 사용량을 색상 격자로 시각화
 → 80% 넘으면 다음 셋 중 하나로 행동

/clear 완전 초기화 (새 작업 시작)
/compact 대화 압축 (맥락 유지)
 /compact focus on auth module ← 특정 영역만 보존
/rewind 시점 단위 되돌리기 (대화 + 코드)
 (별칭: /undo, /checkpoint)
```

**한 줄 운영**:

- 새 피처 → `/clear`
- 같은 피처 계속 + 컨텍스트 무거움 → `/compact`
- 방향 잘못 들었음 → `/rewind`
- 매번 모름 → `/context`로 _현재 상태_ 확인 먼저

[데모: 13-context-tools.html]

---

### 14 라이브 — `/context` 같이 보기

```text
[함께 입력 #2 — 자기 세션 상태 확인]

> /context
```

- 세션이 _비어있으면_ — 위 1강 회수 한 줄을 먼저 입력해 격자에 색이 차게
- 진행자 화면: 토큰 사용량 격자 노출 → _어떤 카테고리가 얼마나 먹는지_ 같이 읽기
- 청중: 자기 PC 격자 확인

**관찰 포인트**:

- _시스템 프롬프트_ 비중 (의외로 큼)
- _MCP 도구 설명_ 비중 (안 쓰면 꺼라)
- _CLAUDE.md_ 비중 (200줄 룰 체감)

[데모: 14-context-live.html]

---

### 15 Plan-Code-Verify 워크플로우

1강에서 본 **하니스 4축**(도구·반복·검증·기억) — Claude Code에서 *살아있는 패턴*이 바로 이거.

```text
Anthropic 공식 4단계

1. Explore Plan Mode 안에서 *관련 코드를 읽기*
2. Plan 구현 계획 작성 → 검토 → 수정
3. Code Auto-Accept로 전환해서 실행
4. Verify 테스트 · 빌드 · 커밋
```

각 단계의 _체크포인트 도구_:

- Explore → `/agents Explore` 서브에이전트로 대량 검색 격리
- Plan → `Ctrl + G`로 외부 에디터에서 plan 직접 수정
- Code → `/diff`로 변경사항 인터랙티브 확인
- Verify → `/rewind`로 안전 되돌리기

[데모: 15-explore-plan-code-verify.html]

---

### 16 TDD 루프 + Hooks

**일상 비유** — 요리.

```text
요리: 재료 손질 → 한 입 맛보기 → 간 조절
 → 한 입 맛보기 → 간 조절
 → 다 됐으면 완성

코딩: 작은 변경 → 테스트 돌리기 → 통과 확인
 → 다음 변경 → 테스트 돌리기 → 통과 확인
 → 다 됐으면 커밋
```

_한 입씩 자주 맛보는_ 셰프와 _마지막에 한 번에 맛보는_ 셰프 — 누가 더 안정적일까요. 같은 원리가 코딩에서 *TDD 루프*입니다.

핵심 5단계:

```text
1. 기능 하나 추가
2. 테스트 돌려서 확인
3. 린트/포맷 체크
4. 문제 없으면 커밋
5. 다음 기능으로 넘어가기
```

→ 문제 생겨도 **마지막 커밋**으로 돌아가면 됨.

[데모: 16-tdd-loop.html]

---

### 17 Hooks 맛보기 — 매번 입력 vs 한 번 박아두기

방금 본 _테스트·린트·커밋_ 루프. 이걸 *매번 입력하지 않고 자동화*해주는 게 **Hooks**.

```text
Before 매번 입력 "코드 수정 → 테스트 → 린트 → 커밋" 4줄 반복
After 한 번 박아둠 파일 편집할 때마다 자동 실행 0줄
```

**살아있는 사례** — 이 강의 레포의 `caveman-kor` hook이 모든 응답에 *"짧은 한국어로"*를 자동 주입 → 출력 토큰 **30~50% 절감**. _"짧게 답해"_ 를 매번 시키지 않고 hook으로 박아둠.

본격적인 *4 이벤트·JSON 구조·다른 활용*은 **3부 27·28 슬라이드**에서. 지금은 _"매번 시킬 일을 한 번 박아둘 수 있다"_ 까지만.

[데모: 17-hooks-teaser.html]

---

### 18 에러 로그 통째로 + Escape 타이밍

**철칙** — 에러를 _해석해서 요약하지 마세요_. 통째로 던져요.

```text
[나쁜 예]
> "Python 코드가 NameError 나는데 변수가 안 잡히는 것 같아"
 ↑ 해석 들어감 → AI도 그 해석에 끌려감

[좋은 예]
> Traceback (most recent call last):
 File "main.py", line 47, in <module>
 result = process(data)
 File "main.py", line 23, in process
 return analyzer.run(items)
 NameError: name 'analyzer' is not defined
 ↑ 통째로 → AI가 *스택 전체*를 자기 시선으로 분석
```

`!` 접두어로 명령 직접 실행도 가능:

```text
> !npm test 2>&1 | tail -100
```

**Escape 타이밍** — Claude의 *thinking 로그*를 보고 *잘못된 가정*이 보이면 **즉시 Escape**. 잘못된 가정 위에 쌓이는 코드는 전부 쓸모없어요. _초반에 잡는 게 핵심_.

[데모: 18-error-logs.html]

---

### 19 docs 폴더 운영 — 이 강의 레포가 살아있는 예시

CLAUDE.md *한 장*은 200줄 한계. 그래서 진짜 깊은 정보는 — **별도 `docs/` 폴더**.

```text
프로젝트 루트/
├── CLAUDE.md (200줄 — 참조만)
└── docs/
 ├── CLAUDE.md (docs/ 작성 가이드)
 ├── concepts/ (LLM·Transformer·바이브코딩 같은 큰 개념)
 ├── techniques/ (프롬프트·컨텍스트·하니스 엔지니어링)
 ├── phenomena/ (환각·시코펀시·Lost-in-the-Middle)
 ├── tools/ (Claude Code · CLAUDE.md · MCP · Skills)
 ├── people/ (Karpathy 같은 인물)
 └── methodologies/ (워터폴·애자일·하이퍼-워터폴)
```

→ CLAUDE.md엔 `@docs/tools/Claude-Code.md` 같은 참조만. *@import는 시작 시 다 로드*되니까 — CLAUDE.md를 짧게 두는 건 _토큰 절약_ 보다 _관리 편의_ 가 본질. 진짜 _lazy load_ (필요할 때만 읽기)는 _Subdirectory CLAUDE.md_(폴더 진입 시) + _Skills_(호출 시) 두 가지.

**일상 비유** — 회사에서 *팀 위키*와 _팀 라이브러리_ 관계. 위키는 _목차_, 라이브러리는 _전체 문서_. 매번 라이브러리를 통째로 외울 필요 없어요.

**문서 주도 개발** _(Documentation-Driven Development)_ — 코드 짜기 전에 _문서 먼저_. 결정·설계가 *영속 가능한 형태*로 남고, 새 세션·새 동료가 *같은 컨텍스트*에서 시작. 자세한 패턴은 `docs/techniques/문서-주도-개발.md`.

[데모: 19-docs-folder.html]

---

### 20 다른 AI에게 비평 받기

막혔을 때 — *같은 모델*에 더 묻지 말고 **다른 AI로 교차 검증**.

```text
/export session.md 파일로 저장
/export --clipboard 클립보드로
/copy 마지막 응답만 복사
/copy 2 마지막에서 2번째 응답만
```

→ 이 텍스트를 ChatGPT나 Gemini에 붙여넣고:

```text
"이 대화를 분석해서, Claude가 놓치고 있는 것이나
 잘못된 접근이 있으면 지적해줘"
```

**왜 통하나** — 모델마다 *학습 데이터·치우침*이 달라요. 같은 문제를 *다른 시선*으로 보면 1강에서 본 _반대 검증_ 효과 ×2.

[데모: 20-cross-llm-review.html]

---

### 21 2부 정리 — 다섯 원칙

```text
1. 한 세션 = 한 피처
2. /context로 *현재 상태* 먼저, 80% 넘으면 행동
3. Plan-Code-Verify 4단계 안에서 산다
4. 테스트는 한 입씩 자주
5. 에러는 통째로, 잘못된 가정엔 Escape
```

2부의 핵심. _외워둘 만한 다섯 줄_.

[데모: 21-part2-summary.html]

---

## 3부 — 자동화 도구 맛보기 

### 22 3부 표지

```text
PART 3 · 

자동화 4부품

Skills · Sub-Agent · Hooks · MCP — 1강에서 맛본 부품들의 본격 풀이

부품당 한 슬라이드씩 — 깊이는 3강에서
```

[데모: 22-part3-cover.html]

---

### 23 Skills — 업무 매뉴얼

1강에서 *템플릿 라이브러리*라고 봤죠. 이제 **구조**를 풀어요.

```text
.claude/skills/
└── ppt-generator/ ← 스킬 폴더
 ├── SKILL.md ← 필수: frontmatter + 지시문
 ├── template.md ← 선택: 템플릿
 └── examples/ ← 선택: 예제

2단계 로딩
 평소 : 이름 + description만 (~50-100바이트)
 호출 시 : 본문 + 참고 파일 전부 로드
```

→ 평소엔 _가볍게_, 쓸 때만 _전체 로드_. CLAUDE.md와 MCP가 *항상 로드*되는 것과 결정적 차이.

**SKILL.md frontmatter 예시**:

```yaml
---
name: ppt-generator
description: "PPT 발표자료 자동 생성. 'PPT 만들어줘',
 '발표자료 작성', '슬라이드 제작' 요청 시 트리거."
---
```

→ description에 _사용자가 쓸 법한 표현 3개 이상_ 박으면 Claude가 _자동 트리거_.

[데모: 23-skills-structure.html]

---

### 24 사전 작성한 Skill 보여주기

라이브 생성은 _너무 많은 변수_ (플러그인 설치·대화형 응답·파일 시스템·권한). 비개발자 진입 위험. **진행자 사전 작성한 작은 skill 한 장**을 화면으로 보여주는 게 안전.

**이 강의 레포에 실제 깔린 skill** — `presentation_slides` (HTML 슬라이드 자동 생성):

```text
.claude/skills/presentation_slides/
└── SKILL.md
 ├── frontmatter (name, description)
 ├── 디자인 시스템 안내 (다크 테마·보라→하늘 그라디언트)
 ├── HTML 보일러플레이트
 └── 절차 (입력 수집 → 슬라이드 목록 확정 → 생성)
```

호출: `> /presentation_slides` 한 줄. *모든 슬라이드 디자인 결정과 절차*가 박혀있어서 _매번 처음부터 안내할 필요 없음_.

**선택지 — 청중 따라하기** _(시간·환경 허락 시)_:

```text
[함께 입력 #3 — 선택]
> /skills 자기 PC의 skill 목록 확인
```

→ 빈 청중도 _"내 PC엔 아직 없구나, 만들면 되겠네"_ 까지만. 라이브 *생성*은 2강 범위 밖, 3강(하니스 세팅)에서 본격.

[데모: 24-skill-live.html]

---

### 25 Sub-Agent — 회사의 부서

1강에서 *회사의 부서*라고 본 그것. 메인 Claude는 PM, 각 서브에이전트는 디자인팀·개발팀·QA팀.

**Claude Code 내장 — 가장 많이 쓰는 3종**:

```text
Explore "이 코드 어디에 있나?" — 탐색 전담 (Haiku, 빠름)
Plan "어떻게 짤지 먼저 보자" — 계획만 세우는 전담
General-purpose "탐색하고 고치고 테스트까지" — 다단계 작업
```

→ 각자 _자기 컨텍스트 창·시스템 프롬프트·도구 권한_. 메인 Claude는 결과 요약만 받음 → **메인 컨텍스트 오염 방지**.

_2개 더_ 있어요 — Bash(별도 컨텍스트 명령 실행) · Claude Code Guide(Claude Code 기능 Q&A). 디테일은 `docs/tools/서브에이전트.md`.

**언제 쓰나** — *대량 출력*이 메인을 오염시킬 작업(전체 테스트 로그·47개 파일 검색). _직접 하기 vs 심부름 시키기_ 판단.

[데모: 25-sub-agents.html]

---

### 26 Hooks — 자동화 엔진

**일상 비유 — 집안의 센서들**. 문 열면 불 켜짐(모션 센서), 차 시동 걸면 안전벨트 경고(시트 센서). _이벤트 → 자동 액션_. Hooks는 Claude Code에서 같은 일을 합니다.

19번에서 _맛만_ 봤죠. 이제 본격 — **이벤트 종류**에 따라 자동화 성격이 달라져요. 가장 많이 쓰는 4가지 + _그 외 다수_ (UserPromptSubmit · SessionStart · SessionEnd · PreCompact · SubagentStop 등).

```text
도구 호출 직전 PreToolUse "이거 진짜 실행해도 돼?"
도구 실행 직후 PostToolUse "끝났네 — 자동으로 lint·포맷"
응답 대기 시 Notification "사용자 응답 기다림 — 알림 보내기"
턴 종료 시 Stop "작업 끝 — 보고서·상태 저장"
 + UserPromptSubmit · SessionStart 등 다수
```

**언제 어느 hook** _(자주 쓰는 것 위주)_:

- **PostToolUse** — 가장 많이 씀. 파일 편집 자동 lint·테스트
- **PreToolUse** — 위험한 명령 미리 차단 (`rm -rf` 같은 거)
- **UserPromptSubmit** — 사용자 prompt에 자동 안내문 주입 (다음 슬라이드 _caveman-kor_ 사례)
- **Notification·Stop** — 알림·기록 (Slack 메시지·로그 저장)

**주의** — Hook 실행 중 Claude는 _멈춰서 기다림_. timeout 꼭 설정, 무거운 작업은 *백그라운드*로 보내야.

[데모: 26-hooks.html]

---

### 27 Hooks — 살아있는 사례 `caveman-kor`

이 강의 레포에 깔린 _진짜로 동작하는_ hook 하나를 봅니다.

```text
caveman-kor UserPromptSubmit 이벤트에 박힌 hook
 기능: 모든 prompt 직후 자동으로 한 줄 주입
 — "짧고 한국어로, 군더더기 빼고 답해라"
 위치: ~/.claude/settings.json (또는 .claude/settings.json)

결과 (지난 6개월 실측)
 출력 토큰 30~50% 감소
 응답 속도 체감 30% 빠름
 설치 비용 settings.json 한 블록 (5~10줄) + 
```

**비유 — 회사의 _기본 안내문_** 같아요. 신입사원에게 매번 _"보고서는 한 장으로, 결론 먼저, 출처 명시"_ 직접 말할 필요 없이 — *팀 가이드*에 한 번 박아두면 자동으로 따라오죠. Hook은 그 *팀 가이드*를 Claude Code 안에서 자동으로 들이미는 장치.

→ 1강에서 본 *하니스 = 모델 주변 환경 전체*의 **가장 작은 단위 사례**. 매일 신경 쓸 일을 *한 줄로 박는다*가 핵심.

[데모: 27-hooks-before-after.html]

---

### 28 MCP — AI 통합의 USB-C

1강에서 본 그 그림 한 줄 더 풀어요.

```text
Anthropic 2024-11 공개
2025-12 Linux Foundation 산하 Agentic AI Foundation에 기증
 → Kubernetes·PyTorch와 같은 중립 인프라로 격상

연결 가능 (2026-05 기준)
 GitHub · Figma · Slack · Google Drive · Notion · Postgres · ...
```

**한 사례 — 토큰 절약 팁**:

- Notion·Linear·Atlassian MCP는 _도구 설명만으로_ 수천 토큰 먹음
- _안 쓰는 MCP는 `/mcp`에서 비활성화_
- `ENABLE_TOOL_SEARCH=1` 환경변수 — 도구 설명 lazy load (필요할 때만 검색)

**MCP vs Skills vs Sub-Agent 한 줄 차이**:

- _MCP_ = 외부 서비스 연결 (항상 로드)
- _Skills_ = 재사용 워크플로우 (lazy load)
- _Sub-Agent_ = 격리된 작업 공간 (호출 시 spawn)

**결정표 — 언제 무엇을 쓰나**:

```text
상황 쓸 도구
─────────────────────────────────────────────────
프로젝트 *전체*에 항상 적용할 규칙 → CLAUDE.md (200줄 룰북)
이 폴더 안 작업에만 적용할 규칙 → Subdirectory CLAUDE.md (lazy)
자주 반복하는 *절차·작업 묶음* → Skills (lazy, /이름)
이벤트마다 자동 실행 (lint·알림·차단) → Hooks (settings.json)
외부 서비스 연결 (GitHub·Figma·DB) → MCP
대량 출력·격리된 분석 → Sub-Agent (/agents)
```

→ _"매번 직접 시키지 않고 어디에 박을까"_ 결정 시 위 표 한 장만.

[데모: 28-mcp-decision.html]

---

## 4부 — 마무리 

### 29 오늘의 압축 — 한 장

```text
1부 기본기 Plan Mode (Shift+Tab × 2)
 CLAUDE.md (200줄, CRITICAL, @import)
 안전망 (/sandbox · /permissions · /rewind)

2부 실전 한 세션 = 한 피처
 컨텍스트 4도구 (/context · /clear · /compact · /rewind)
 Plan-Code-Verify 4단계
 에러는 통째로, 잘못된 가정엔 Escape
 docs/ 폴더로 *문서 주도 개발*

3부 자동화 Skills (재사용 워크플로우, /skills)
 Sub-Agent (5종 내장, /agents)
 Hooks (4 이벤트, /hooks)
 MCP (USB-C, /mcp)
```

→ **이 한 장이 오늘의 압축**. 인쇄해서 책상 옆에 붙여두세요.

[데모: 29-summary.html]

---

### 30 다음 강의 예고 — 3강

오늘 *도구 자체*를 마스터했어요. 다음 시간은 그 도구를 **내 프로젝트 위에 진짜로 한 층 올리는 법**.

```text
3강 — 하니스 세팅

내 프로젝트에 2층 한 층 더 올리기 — 4종 markdown만 손봐도 충분

 CLAUDE.md 이 프로젝트의 룰북
 docs/ PRD · ADR · UI_GUIDE 4종
 skills/ /harness · /review 같은 재사용 워크플로우
 hooks/ caveman-kor 같은 출력 토큰 절감 hook

클라이맥스 — claude -p 매커니즘 (CI/CD에 헤드리스 Claude 끼우기)

그리고 4강 — Dicom Viewer 만들기 (5단계 워크플로우 라이브)
```

오늘 강의 끝. 감사합니다.

[데모: 30-next-lecture.html]

---

## 강사 노트 — 발표 전 체크리스트

### 1강 회수 포인트 매핑 _(슬라이드 본문에는 노출 X)_

| 2강 슬롯 | 1강 회수 슬롯 | 회수 내용 |
| -------- | ------------- | -------------------------------- |
| 02 | 30·33 | 동심원 그림 |
| 04 | 43 | CLAUDE.md _팀 룰북_ 비유 |
| 10 | — | Auto Mode 차단 사례 (자체 일화) |
| 12 | 36 | Lost in the Middle |
| 15 | 39 | 하니스 4축 (도구·반복·검증·기억) |
| 20 | 25 | 반대 검증 (시코펀시) |
| 23 | 44 | Skill _템플릿 라이브러리_ |
| 26 | 45 | 서브에이전트 _회사 부서_ |
| 29 | 45 | MCP _USB-C_ |

### 3종 패키지 누락 체크

| 개념 | 일상 비유 | Before/After | 라이브·사례 |
| -------------- | ------------------------ | -------------------------------- | ------------------------------- |
| Plan Mode | ✅ 건축 도면 | ✅ 즉시 실행 vs /plan | ✅ 라이브 시연 |
| 모드 4종 | — | — | ✅ Auto Mode 차단 사례 |
| CLAUDE.md | ✅ 팀 룰북·내 책상 메모 | ✅ 직접 작성 vs @import | ✅ [함께 입력 #1] /init |
| 컨텍스트 4도구 | — | — | ✅ [함께 입력 #2] /context |
| TDD 루프 | ✅ 요리 — 한 입씩 | ✅ 매번 입력 vs Hook | — |
| docs 폴더 | ✅ 팀 위키·라이브러리 | — | ✅ 이 레포 자체 |
| Skills | (1강 슬롯 44 회수) | — | ✅ [함께 입력 #3] skill-creator |
| Sub-Agent | (1강 슬롯 45 회수) | — | ✅ 내장 5종 표 |
| Hooks | ✅ 센서 (모션·시트) | ✅ 매번 입력 vs UserPromptSubmit | ✅ caveman-kor |
| MCP | (1강 슬롯 45 USB-C 회수) | — | ✅ 토큰 절약 팁 |

핵심 6개(Plan Mode · CLAUDE.md · 컨텍스트 관리 · Skills · Sub-Agent · Hooks) 모두 _최소 2종 이상_ ✓

### 시점 의존 단어 grep

```bash
grep -n "최근\|요즘\|올해\|현재" v2/2강/script.md
```

→ 0건이어야 함

### 버전 신선도

- Claude Code v2.1.x
- 모델: Opus 4.7 / Sonnet 4.6 / Haiku 4.5
- MCP Linux Foundation 기증 = 2025-12
- 발표 직전 `docs/tools/Claude-Code.md` 헤더와 1회 교차 검증
