# Claude Code Hooks (훅)

> *어떤 사건이 일어날 때마다 자동으로 실행되는 행동*. CLAUDE.md/docs/skills가 *"미리 알려주거나 호출해서 실행되는 정보·절차"*라면, Hooks는 *"여러분이 시키지 않아도 알아서 일어나는 일"*. **2층 하니스의 4번째 레이어 = 자동 반사**.

## 1. 왜 "Hook(훅)"이라고 부르나

- **Hook**: 영어로 *"걸쇠·갈고리"*. 컴퓨팅에서는 오래전부터 *"특정 이벤트가 발생할 때 끼어들어 코드를 실행하는 지점"*을 가리키는 표준 용어 (예: 워드프레스의 action/filter hook, git 의 pre-commit hook).
- Claude Code의 hook도 같은 개념을 그대로 가져왔다 — **세션의 특정 시점에 외부 스크립트가 끼어들 수 있는 지점**.
- **언제 등장했나**: Claude Code가 출시(2025-02)된 후 추가된 기능. 2026년 현재는 *12종 라이프사이클 이벤트*가 공식 문서에 명시.

## 2. 그전에는 어떤 문제가 있었나

LLM 기반 도구는 *모든 행동을 모델이 결정*하는 구조였다. 하지만 실무에서는 — *"이 명령은 절대 통과시키면 안 돼"*, *"매 응답이 끝날 때마다 한국어 톤 검사를 자동으로 돌려"* 같은 **결정론적 규칙**이 필요한 순간이 많다.

- 모델은 *확률적*이라 100% 신뢰하기 어렵다 (→ [비결정성](../phenomena/비결정성.md))
- 매번 사람이 검토할 수도 없다
- 시스템 프롬프트에 더 적기에는 — 텍스트가 너무 길어지고, 모델이 무시할 수도 있다

**일상 비유**: 회사 출입문에 *지문 인식기*를 다는 것과 같다. *"보안에 신경 쓰세요"* 라고 매뉴얼에 적는 대신, **어떤 사건(=출입 시도)에 대해 자동으로 작동하는 결정론적 장치**를 설치한다. 사람의 의지·기억력에 기대지 않는다.

## 3. 어떻게 해결했나

Hooks는 모델 *바깥*에서 동작하는 **결정론적 제어 레이어**다. Claude Code 세션 안의 12개 라이프사이클 이벤트마다 외부 스크립트(셸·파이썬·뭐든)를 자동 실행할 수 있다.

### 12개 이벤트 (3가지 cadence)

```text
세션 단위 (1회)
  SessionStart        세션 열림
  SessionEnd          세션 종료

응답 단위 (턴마다)
  UserPromptSubmit    사용자 입력 도착
  Stop                Claude의 응답 생성 완료
  StopFailure         응답 실패

도구 호출 단위 (도구마다)
  PreToolUse          도구 실행 직전 (유일하게 차단 가능)
  PostToolUse         도구 실행 직후
  ... (기타 4종)
```

### 설정 방법

`.claude/settings.json` 한 줄로 등록:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": ".*",
        "hooks": [{"type": "command", "command": "caveman-kor"}]
      }
    ]
  }
}
```
- 프로젝트 단위: `.claude/settings.json` (팀과 공유)
- 사용자 단위: `~/.claude/settings.json` (개인용)

### 차단 가능 vs 단순 후처리

- **PreToolUse만이 차단할 수 있다**. 훅 스크립트가 exit code 2로 종료하면 도구 호출이 막히고, stderr가 모델에게 *오류 메시지*로 피드백된다.
- 나머지 이벤트는 후처리·관찰 용도.

## 라이브 시연 가능한 예시 — `caveman-kor`

이번 강의 레포가 실제로 사용하는 hook이다.

### 문제 — 한국어 응답이 길어진다
한국어로 질문하면 Claude가 친절하게 길게 답한다. *같은 작업*인데도 영어 대비 출력 토큰이 1.5~2배. 비용 누적.

### 해결 — `Stop` 이벤트에 `caveman-kor` 등록
응답이 끝날 때마다 자동으로 *"군더더기 빼고, 핵심만 남겨라"* 후처리.

### Before / After
```text
[BEFORE — 일반 응답]
  "네, 알겠습니다! 말씀하신 부분에 대해서 자세히 설명드리면,
   먼저 첫 번째로 …(이하 200자) … 이런 흐름으로
   진행하시면 됩니다."

[AFTER — caveman-kor 훅 적용]
  "Phase 1 완료. 다음. Phase 2 시작."
```

### 효과 — **출력 토큰 30~50% 절감**
같은 작업·같은 품질, 출력 토큰만 반토막. 비용도 그만큼 절감.

## Before/After — Hook 유무

| 상황 | Hook 없음 | Hook 있음 |
|---|---|---|
| 위험한 명령 차단 | 매번 사람이 검토 | `PreToolUse`로 자동 차단 |
| 응답 톤 통일 | 매 세션 같은 지시 반복 | `Stop` 훅으로 자동 후처리 |
| 코드 변경 후 테스트 | 사용자가 수동 실행 | `PostToolUse`로 `pytest` 자동 실행 |
| TDD 강제 | "테스트 먼저 짜" 매번 잔소리 | `tdd-guard` 훅이 테스트 없는 코드 변경 차단 |

## 실제 사례 — 자주 쓰이는 hook 패턴

- **`tdd-guard`** (PreToolUse): Edit·Write 시 대응 테스트 파일이 없으면 차단
- **`dangerous-cmd`** (PreToolUse): `rm -rf`·`drop database` 같은 명령에 대해 추가 확인 강제
- **`caveman-kor`** (Stop): 한국어 응답 압축 (이번 강의 레포)
- **`git-auto-stage`** (PostToolUse): Edit 후 변경 파일 자동 git add
- **자동 테스트 러너** (Stop): Phase 종료 시 `pytest`/`npm test` 자동 실행

## 1·2강 강의 연결 포인트

- **1강**: 직접 언급 없음.
- **2강 #14** [데모: 14-hooks.html] — 정확히 이 문서의 본문. `caveman-kor` 사례를 중심으로 *"여러분이 시키지 않아도 알아서 일어나는 일"* 메시지.
- **2강 #15** [데모: 15-framework-complete.html] — 4번째 레이어로 hooks 등장 (`caveman-kor`, `tdd-guard`, `dangerous-cmd`).
- **2강 #16** [데모: 16-two-layers-combined.html] — 2층의 4번째 요소.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code](Claude-Code.md) — Hook 호스트
- [Claude-Code 1층 하니스](Claude-Code-1층-하니스.md) — 1층의 *권한 체크*가 강제 차단을 담당, 2층의 PreToolUse hook은 *프로젝트 맞춤* 차단
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — Hook은 하니스의 *결정론적* 부분
- [비결정성](../phenomena/비결정성.md) — Hook은 모델의 비결정성을 *바깥에서 결정론으로 둘러싸는* 장치

## 출처

- [Anthropic — Hooks reference (Claude Code Docs)](https://code.claude.com/docs/en/hooks) — 12개 이벤트 공식 명세
- [Claude Code Hooks: Complete Guide to All 12 Lifecycle Events (claudefa.st)](https://claudefa.st/blog/tools/hooks/hooks-guide) — 이벤트별 cadence 정리
- [Pixelmojo: Claude Code Hooks — PreToolUse, PostToolUse & Stop](https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns) — 차단·exit code 동작
- [Claude Code Hooks Complete Guide (March 2026 Edition)](https://smartscope.blog/en/generative-ai/claude/claude-code-hooks-guide/) — 2026 기준 사례 모음
- [Vincent's Blog: Claude Code settings.json Deep Dive — The Hooks System](https://blog.vincentqiao.com/en/posts/claude-code-settings-hooks/) — 설정 파일 구조
