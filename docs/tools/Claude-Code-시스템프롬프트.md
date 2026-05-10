# Claude Code 시스템 프롬프트 (System Prompt)

> Claude Code가 매번 모델에게 미리 들려주는 **안전장치 텍스트**. 1층 내장 하니스의 가장 핵심 요소이며, **2025년 2월·2026년 3월** 두 번에 걸쳐 유출되면서 전체 모습이 공개됐다.

## 1. 왜 "시스템 프롬프트"라고 부르나

- **System prompt**: 사용자가 보낸 메시지가 도착하기 *전에* 모델에게 미리 주입되는 지시문. 채팅 GPT가 등장한 2022년 말부터 OpenAI·Anthropic이 표준화한 용어.
- 채팅창에는 보이지 않지만, 모든 응답의 **밑그림**을 깐다. 비유하자면 — *영화 감독이 배우들에게 촬영 전에 따로 알려주는 캐릭터 설정·금지사항* 같은 위치.
- Claude Code의 시스템 프롬프트는 한 단계 더 나아간다. 단순한 "친절하게 답하라" 수준이 아니라, **위험한 명령 차단·도구 사용 규칙·git 안전수칙**이 텍스트로 명시돼 있다.

## 2. 그전에는 어떤 문제가 있었나

LLM이 코드 작성 도구로 등장하던 초기(2022~2024년) — 모델은 "코드를 짤 수 있다"는 능력은 가졌지만, **무엇을 하면 안 되는지에 대한 가드레일이 없었다**.

- AI가 자기 판단으로 `git push --force` 같은 파괴적 명령을 실행
- 사용자가 명시하지 않은 파일까지 멋대로 삭제
- "보안 검토" 같은 민감 작업에서도 거리낌 없이 답변

**일상 비유**: 갓 입사한 인턴에게 *모든 권한*을 부여한 회사. 똑똑하지만 *"이거는 절대 손대면 안 돼"* 라는 규정집이 없으면, 좋은 의도로 한 행동이 큰 사고로 이어진다. 시스템 프롬프트는 그 인턴에게 **첫날 건네는 사규집**이다.

## 3. 어떻게 해결했나

Anthropic은 Claude Code를 출시(2025년 2월 24일)하면서 — 시스템 프롬프트에 **수십 가지 행동 규칙**을 명시적으로 박아 넣었다. 핵심은 두 가지 패턴.

**A. NEVER / DO NOT 패턴**
> 언어 모델은 *"조심해라"* 보다 *"절대 하지 마라"* 에 더 강하게 반응한다. 그래서 Claude Code 시스템 프롬프트는 **NEVER·DO NOT·CRITICAL** 같은 강한 부정형을 의도적으로 사용.

**B. Git Safety Protocol** (가장 자주 인용되는 부분)
```text
- NEVER update the git config
- NEVER run destructive git commands (push --force, reset --hard,
  checkout ., restore ., clean -f, branch -D) unless explicitly requested
- NEVER skip hooks (--no-verify, --no-gpg-sign) unless explicitly requested
- NEVER run force push to main/master, warn the user if they request it
- CRITICAL: Always create NEW commits rather than amending,
  unless the user explicitly requests a git amend
- NEVER use git commands with the -i flag (interactive mode unsupported)
```

이 규칙들은 *"AI가 혼자 일하다 저지를 수 있는 가장 위험한 git 사고"* 를 처음부터 막는다. **여러분이 Claude Code를 실행하는 순간, 이 안전장치는 이미 작동하고 있었다.**

## 두 번의 유출 — 시스템 프롬프트가 어떻게 공개됐나

### 1차 유출: 2025년 2월 24일 (Claude Code 출시일)

- **무엇이 새어 나갔나**: 1,800만 자(18M characters) 분량의 **인라인 소스맵**이 npm 패키지 `@anthropic-ai/claude-code` 안에 포함된 채 배포.
- **얼마나 노출됐나**: 발견 후 약 **2시간 만**에 Anthropic이 패키지를 내림.
- **반응**: 시스템 프롬프트 일부 + 도구 정의가 부분 공개. 커뮤니티는 "AI가 어떻게 안전장치를 받는지 처음으로 들여다봤다"고 평가.

### 2차 유출: 2026년 3월 31일 (대규모, 현재 강의 기준)

- **무엇이 새어 나갔나**: 59.8 MB짜리 **`.map` 소스맵 파일**이 npm 버전 `@anthropic-ai/claude-code` v2.1.88에 그대로 포함됨. 설정 파일에서 한 줄이 누락된 게 원인.
- **얼마나 노출됐나**: 약 **2,000개 TypeScript 파일·512,000 줄**의 전체 코드. 시스템 프롬프트 *전문* + 24개 빌트인 도구 정의 + 서브에이전트 프롬프트(Plan/Explore/Task) + 유틸 프롬프트(CLAUDE.md, compact, statusline 등) 모두 노출.
- **타임라인**: 2026-03-30~31 새벽 npm에 push → 03-31 오전 4:23 ET, Solayer Labs의 한 인턴이 X에 발견 사실 게시 → 수 시간 내 수천 명이 GitHub로 미러링·분석.
- **추가로 드러난 것들**:
  - **Undercover Mode**: Anthropic이 오픈소스 레포에 *익명으로 기여*할 때 쓰는 모드. 시스템 프롬프트에 *"You are operating UNDERCOVER... Your commit messages MUST NOT contain ANY Anthropic-internal information. Do not blow your cover."* 라고 명시.
  - **KAIROS**: 출시되지 않은 *자율 데몬 모드*. 소스에 150회 이상 언급. 백그라운드 에이전트가 세션을 넘어 지속되며 주기적 tick 프롬프트를 받아 GitHub webhook 모니터링·알림 발송 같은 행동을 *스스로* 결정.
  - **Hook 오케스트레이션 로직 + MCP 서버 처리 코드** 전부 노출 — 보안 측면에서 악성 레포가 Claude Code를 속여 백그라운드 명령 실행을 유도할 길이 열림.

### 비교

| 항목 | 1차 (2025-02) | 2차 (2026-03) |
|---|---|---|
| 포맷 | 인라인 소스맵 | `.map` 파일 |
| 분량 | 18M chars | 59.8 MB · 512,000 줄 |
| 발견~조치 | ~2시간 | 수 시간 내 미러링 완료 (회수 사실상 불가능) |
| 노출 범위 | 시스템 프롬프트 일부 + 도구 일부 | **거의 전부** — 시스템 프롬프트 전문, 모든 도구, 미공개 기능까지 |

## 라이브 시연 가능한 예시

### 예시 1 — "Force push 시켜봐" 요청
```text
[강의 중 라이브 시연]

USER: claude code에게 "main 브랜치에 force push 해줘" 입력
EXPECTED: AI가 *"NEVER force push to main/master 규칙 때문에 거부합니다.
          따로 브랜치를 만들거나, 의도를 명확히 알려주세요"* 라고 답변

→ 청중은 그 거부 메시지가 *어디서 왔는지* 알게 된다 — 시스템 프롬프트.
```

### 예시 2 — Before/After (시스템 프롬프트 유무)
```text
BEFORE  (안전장치 없는 일반 LLM API 직접 호출)
  USER: "이 디렉토리 다 지워줘"
  AI:   `rm -rf .` 즉시 실행 → 데이터 소실

AFTER   (Claude Code = 시스템 프롬프트 적용)
  USER: "이 디렉토리 다 지워줘"
  AI:   "정말 지울까요? 되돌릴 수 없는 작업입니다.
        다음 파일이 영향받습니다: ... [확인 요청]"
```

### 예시 3 — 직접 시스템 프롬프트 내용 확인
강의 중에 GitHub에서 `asgeirtj/system_prompts_leaks/Anthropic/claude-code.md` 를 열어 한 페이지를 청중에게 직접 보여줄 것. 영어 그대로지만, "NEVER force push", "ALWAYS create NEW commits" 같은 단어가 *대문자*로 박혀 있는 게 한눈에 보인다.

## 1·2강 강의 연결 포인트

- **1강**: 직접 언급 없음. 1강은 환각·비결정성·토큰화 등 *모델의 한계* 에 집중.
- **2강 #2** [데모: 02-system-prompt-leak.html]: 정확히 이 문서가 다루는 내용. 2026년 3월 유출 사건을 도입부로 쓰고, *"이 안전장치는 여러분이 Claude Code를 실행하는 순간 이미 깔려 있었다"* 라는 메시지로 1층(내장 하니스) 개념을 처음 소개.
- **2강 #3** [데모: 03-other-builtin.html]: 시스템 프롬프트 외에도 권한 체크·도구 경계·JSON 스키마 등 *다른 1층 요소들* 이 함께 등장. 이 문서는 그 중 첫 번째이자 가장 두꺼운 한 장에 해당.
- **2강 #16** [데모: 16-two-layers-combined.html]: "1층 = 시스템 프롬프트·권한체크·도구경계·JSON스키마" 4가지 통합 그림. 시스템 프롬프트는 그 중 *맨 앞에 깔리는 가장 큰 안전장치*.

## 꼬리에 꼬리 (관련 개념)

- [Claude Code](Claude-Code.md) — 시스템 프롬프트의 호스트 도구
- [CLAUDE.md](CLAUDE-md.md) — 사용자가 추가하는 *2층* 컨텍스트. 시스템 프롬프트(1층)와 결합되어 모델 입력 구성
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — 시스템 프롬프트는 컨텍스트 엔지니어링의 *최저층 사례*
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — 시스템 프롬프트 = 하니스의 1층(내장)

## 출처

- [GitHub: asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks) — 시스템 프롬프트 추출 모음, 정기 갱신 (Opus 4.7·Claude Code 등)
- [GitHub: Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) — Claude Code 버전별 시스템 프롬프트·24개 빌트인 도구·서브에이전트 프롬프트 전체
- [VentureBeat: Claude Code source code appears to have leaked (2026-03)](https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know) — 2026년 3월 유출 1차 보도
- [Alex Kim: The Claude Code Source Leak — fake tools, frustration regexes, undercover mode (2026-03-31)](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/) — Undercover Mode 분석
- [InfoQ: Anthropic Accidentally Exposes Claude Code Source via npm Source Map File](https://www.infoq.com/news/2026/04/claude-code-source-leak/) — 사고 원인·타임라인 정리
- [the-ai-corner.com: Claude Code Source Code Leaked — What's Inside (2026)](https://www.the-ai-corner.com/p/claude-code-source-code-leaked-2026) — KAIROS·Hook 로직 분석
- [Penligent: Claude Code Source Map Leak — What Was Exposed and What It Means](https://www.penligent.ai/hackinglabs/claude-code-source-map-leak-what-was-exposed-and-what-it-means/) — 1차(2025-02) + 2차(2026-03) 비교
- [DEV: The Great Claude Code Leak of 2026 (varshithvhegde)](https://dev.to/varshithvhegde/the-great-claude-code-leak-of-2026-accident-incompetence-or-the-best-pr-stunt-in-ai-history-3igm) — 사고·반응 종합
- [Aiia: Claude Code System Prompt Leaked — Full Breakdown](https://aiia.ro/blog/claude-code-system-prompt-leaked/) — Git 규칙 인용
