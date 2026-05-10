# Permissions & Hooks (퍼미션과 훅)

> *모델이 무엇을 *언제* 할 수 있는가*. 안전과 자율의 균형. **하니스의 *문지기와 자동 반사***. 1층 하니스(시스템 박힘) + 2층 하니스(프로젝트별 추가) 가 결합되는 자리.

> 부모 문서: [하니스 엔지니어링](../하니스-엔지니어링.md)

## 1. 정의

**Permissions** = 도구 호출·파일 변경·외부 통신 같은 *행동*에 대한 *허가 체계*. 사용자 확인·자동 승인·완전 차단 등.

**Hooks** = 특정 이벤트(도구 호출 직전·응답 끝·세션 시작 등)에 *자동으로 끼어드는* 결정론적 매커니즘. 모델 *바깥*에서 작동.

둘 다 **모델의 비결정성을 결정론으로 둘러싸는** 역할.

## 2. 그전에는 어떤 문제가 있었나

LLM 만으로는 *안전*과 *자율* 사이 양자택일.

- 모든 행동에 사용자 확인 → 너무 느림 (200번 다이얼로그 = 사고도 못함)
- 모든 행동 자유 → 사고 위험 (`rm -rf` 한 줄에 데이터 소실)
- 모델이 *상황 판단* 으로 결정 → 비결정적·환각 위험

→ *결정론적 가드*가 필요했다.

**일상 비유**: 회사 출입 시 *지문 인식기*. *"보안 신경 쓰세요"* 매뉴얼 ❌. *"매번 자동으로 검사"* ✅. Permissions·Hooks 가 정확히 그 *결정론적 검사*.

## 3. 두 축 자세히

### (A) Permissions — 허가 체계

Claude Code 의 **5+1 모드** (자세히는 [퍼미션 모드](../../tools/Claude-Code-퍼미션모드.md)):

```text
plan       읽기만, 실행 ❌
default    매 위험 행동 확인
acceptEdits 편집 자동, 시스템 명령 확인
auto       분류기가 자동 판단 (Team plan)
bypass     모든 확인 스킵 (위험)
+
dontAsk   특정 도구·패턴 등록 항상 허용
```

**우선순위 위계**:
```text
높음 ↑
  Anthropic 안전 정책 (모델 내재)
  System prompt 의 NEVER 규칙
  사용자 settings.json 의 dontAsk
  현재 모드 (plan/default/...)
  Hook 의 PreToolUse 차단
낮음 ↓
```

→ 위쪽이 우선. 사용자가 *"force push 해도 돼"* 라고 해도 시스템 prompt 가 거부.

### (B) Hooks — 자동 반사

Claude Code 의 **12 라이프사이클 이벤트** (자세히는 [Hooks](../../tools/Claude-Code-Hooks.md)):

```text
세션      SessionStart, SessionEnd
응답      UserPromptSubmit, Stop, StopFailure
도구      PreToolUse  ← 차단 가능
          PostToolUse, ...
```

`PreToolUse` 만 *차단 가능*. exit code 2 + stderr 가 모델에 피드백.

### 둘의 결합 — 4단 방어선

```text
모델이 'rm -rf .' 호출 의도

[방어 1] System prompt: 'NEVER run rm -rf' 가 모델에 박힘
         → 모델이 *시도 자체*를 안 함

[방어 2] (그래도 시도하면) JSON 스키마 검증
         → 도구 호출 형식 확인

[방어 3] PreToolUse hook: 'rm -rf 패턴 차단' 등록
         → exit 2 → 차단 + "더 안전한 명령 써라" 메시지

[방어 4] (hook 통과해도) 퍼미션 모드:
         default → 사용자 확인 다이얼로그
         → 사람이 마지막 결정
```

같은 위험이 *4번* 검증됨. 1+2층 하니스가 결합된 *입체 방어*.

## Before / After

```text
[BEFORE — Permissions·Hooks 없는 LLM API]
USER: "이 폴더 정리해줘"
AI:   [Bash 호출 → rm -rf .]
      → 파일 모두 삭제 (사고)

[AFTER — Claude Code (1층 + 2층)]
USER: "이 폴더 정리해줘"
AI:   [Bash 호출 의도]

방어 1: System prompt 거부 → "위험. 더 안전한 방법 제안"
방어 2: PreToolUse hook → 패턴 차단
방어 3: 퍼미션 default → "정말 실행할까요?" 다이얼로그

→ 사람이 거부 가능. 사고 차단.
```

## 라이브 시연 가능한 예시

### 시연 1 — PreToolUse hook 작동
```bash
[settings.json 에 등록]
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "scripts/dangerous-cmd-guard.sh"}
        ]
      }
    ]
  }
}

[강의 중]
> "이 폴더 다 지워줘"
[Claude → Bash 'rm -rf .' 호출 의도]
[Hook 발동 → exit 2 → "rm -rf 차단됨"]
[stderr → 모델에 피드백]
[Claude] "rm -rf 가 차단되었습니다. 대신:
         1) 특정 파일만 삭제
         2) 백업 후 진행
         어떻게 할까요?"
```

### 시연 2 — 퍼미션 모드 전환
```bash
[default 모드] 매번 확인 → 30번 다이얼로그
[Shift+Tab → acceptEdits] → 편집은 자동, 위험 명령만 확인
[Shift+Tab → plan] → 실행 ❌, 계획만 출력
```

청중에게: *"같은 작업이 모드 전환만으로 *완전히 다른 안전성*을 가진다"*.

## 4. 실제 사례

- **Claude Code 자체** — 1층(시스템 prompt) + 1층(권한 체크) + 2층(hooks) 가 표준
- **`tdd-guard` hook** — TDD 강제 (테스트 없는 코드 변경 차단)
- **`dangerous-cmd-guard` hook** — `rm -rf`·`drop database`·force-push 차단
- **`secret-scanner` hook** — git commit 시 `.env`·API key 노출 자동 차단
- **2026-03 유출 이후 강화**: `Comment and Control` 같은 prompt injection 공격 사례 (VentureBeat 2026-04 보도) 이후 — *PreToolUse hook + 도구 화이트리스트* 가 *기본 권장*

## 한계

- **너무 엄격한 hook → 사용 불편**: 모든 명령 차단하면 작업 불가. 균형 필수.
- **Hook 작동 못함 케이스**: bypassPermissions 모드는 일부 hook 도 우회. **bypass 는 정말 필요할 때만**.
- **Hook 의 stderr 가 모델 컨텍스트로 들어감 → 토큰 폭증**: 긴 오류 메시지는 컨텍스트 오염.
- **사용자 피로**: 너무 자주 묻는 default 모드는 사용자가 *습관적 yes* 누름 (실제 위험 못 인지). → `auto` 모드의 분류기가 푸는 문제.

## 꼬리에 꼬리 (관련 개념)

- [하니스 엔지니어링](../하니스-엔지니어링.md) — 부모 문서
- [Tools](tools.md) — Permissions·Hooks 가 *어떤 도구*에 작동하는지
- [Evaluation Loop](evaluation-loop.md) — Hook 으로 *검증 자동 발화* 가능
- [Control & State](control-and-state.md) — Phase 게이트와 결합
- [Claude Code 1층 하니스](../../tools/Claude-Code-1층-하니스.md) — 1층의 시스템 prompt + 권한 체크
- [Claude Code Hooks](../../tools/Claude-Code-Hooks.md) — Hook 자체의 도구 측 deep dive
- [퍼미션 모드](../../tools/Claude-Code-퍼미션모드.md) — 5+1 모드의 deep dive
- [Claude Code 시스템프롬프트](../../tools/Claude-Code-시스템프롬프트.md) — 1층 NEVER 규칙들

## 출처

- [Anthropic — Choose a permission mode](https://code.claude.com/docs/en/permission-modes) — 퍼미션 표준
- [Anthropic — Hooks reference](https://code.claude.com/docs/en/hooks) — Hook 표준
- [VentureBeat — Three AI coding agents leaked secrets through prompt injection (2026-04)](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) — 보안 사고 분석
- [Dotzlaw — Claude Code Hooks: The Deterministic Control Layer for AI Agents](https://www.dotzlaw.com/insights/claude-hooks/) — Hook 의 결정론 역할
