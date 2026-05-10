# Control & State (제어와 상태)

> *작업을 어떻게 쪼개고·언제 멈추고·무엇을 *기억해* 넘길까*. 하니스의 *프로젝트 매니저*. **Phase 분할 + docs 영속화 + 워크트리 격리**.

> 부모 문서: [하니스 엔지니어링](../하니스-엔지니어링.md)

## 1. 정의

Control = *작업의 분할·스케줄링·종료 조건* 결정
State = *각 단계 사이에 무엇을 기억해 다음으로 넘길지* 영속화

LangChain·Anthropic 의 정의:
> *"Harness specifies (i) control: how work is decomposed and scheduled; (ii) contracts: what artifacts must be produced, what gates must be satisfied, and when the run should stop; and (iii) state: what must persist across steps, branches, and delegated workers."*

→ 줄여서 **C + C + S** (Control · Contracts · State).

## 2. 그전에는 어떤 문제가 있었나

LLM이 *큰 작업*을 한 번에 시도하면:

- 컨텍스트 창 폭발
- 중간에 흐름 끊김 → 다시 시작 시 *처음부터*
- 작업이 *끝났는지 끝났다고 착각인지* 판단 모호
- 병렬 작업이 서로의 파일을 덮어씀

→ *작업의 분해·상태 관리·종료 기준* 이 명시적으로 필요했다.

**일상 비유**: 큰 프로젝트는 *PM*이 있다. *Phase 쪼개기, 산출물 정의, 완료 기준 합의, 회의록 보관*. C+C+S 가 정확히 그 *PM 역할*.

## 3. 세 축 자세히

### (A) Control — 작업 분할

**Phase 분할 (Decomposition)**
큰 작업을 *수 시간 단위 작업*으로 쪼갬. 각 phase는 독립적으로 실행 가능.

```text
"DICOM Viewer 만들기"
  → Phase 1: 폴더 구조 + 기본 파일
  → Phase 2: DICOM 파서
  → Phase 3: UI 골격
  → Phase 4: 측정 도구
  → Phase 5: 주석 시스템
```

**스케줄링 (Scheduling)**
- *순차*: Phase 1 → 2 → 3 (의존성 있을 때)
- *병렬*: 독립 phase는 동시 실행 (워크트리 격리)
- *조건부*: Phase 3 결과에 따라 4 또는 4'

### (B) Contracts — 산출물·게이트·종료

**산출물 (Artifacts)**: 각 phase가 *반드시 만들어야 할* 결과
**게이트 (Gates)**: 다음 phase로 넘어가기 *전에 통과해야 할* 검증
**종료 조건 (Stop Criteria)**: *언제* 전체 작업이 끝났다고 판단할지

```text
Phase 2: DICOM 파서
  Artifact: src/parser.py + tests/test_parser.py
  Gate: pytest 통과 + 100ms 이내 1MB 파싱
  Stop: 전체 phase 5/5 + 통합 테스트 통과
```

### (C) State — 상태 영속화

각 phase가 *다음 phase에게 무엇을 넘길지*. **헤드리스 모드의 무기억 한계**를 푸는 핵심.

**영속화 매체**:
- `docs/` 4종 문서 (PRD·ARCHITECTURE·ADR·UI_GUIDE) — 결정의 영속화
- `phases/{task}/` — phase별 상태·결과·로그
- `working/` 보고서 — 각 phase 종료 시 자동 작성
- `report/` 최종 — 통합 결과
- `feedback/` 사람 피드백 — 다음 시도에 반영
- `troubleshootings/` — 발견된 함정 (재발 방지)

→ 자세히는 [하이퍼-워터폴](../../methodologies/하이퍼-워터폴.md) 의 7폴더 체계.

## Before / After

```text
[BEFORE — Control 없음]
USER: "DICOM Viewer 만들어줘"
AI:   [한 응답에 모든 코드 시도]
      → 컨텍스트 폭발 / 중간에 흐름 끊김 / 결과 신뢰 ↓

[AFTER — C+C+S 적용 (`/harness`)]
USER: "/harness"
1) 자동: docs/ 읽기 (PRD·ARCH·ADR)
2) 자동: 5개 phase 분할 + 산출물 명시
3) 자동: phase 1 헤드리스 호출 → 결과 working/ 저장
4) 자동: phase 2 (이전 phase 의 working/ 보고서 + docs 컨텍스트로) → ...
5) 자동: 5/5 완료 → report/ 통합
17분 후: "완료. 54개 테스트 통과"
```

→ **상태가 docs/ 에 영속**되기 때문에 — 헤드리스 *무기억* 매번 새 Claude도 *프로젝트 전체*를 이해.

## 라이브 시연 가능한 예시

```bash
[강의 중 — execute.py 실행 직후]
$ ls phases/dicom-viewer/

phase-1.md         (계획)
phase-1.complete   (완료 표시)
phase-2.md
phase-2.complete
...
phase-5.md
phase-5.complete

$ cat phases/dicom-viewer/phase-1.complete
{
  "started_at": "2026-05-10T10:23:11",
  "completed_at": "2026-05-10T10:26:11",
  "duration_sec": 180,
  "artifacts": ["src/parser.py", "tests/test_parser.py"],
  "tests_passed": 12
}
```

청중에게: *"각 phase 가 *독립*하지만, *상태 파일*로 다음 phase에 *연결*된다."*

## 4. 워크트리 격리 (Worktree Isolation)

병렬 phase가 *서로의 파일을 덮어쓰지 않게* 분리하는 매커니즘.

```text
프로젝트 루트
  ├── (메인 워크트리)
  ├── .git/worktrees/phase-2/   ← phase 2 전용 격리
  └── .git/worktrees/phase-3/   ← phase 3 전용 격리

phase-2 와 phase-3 가 *동시* 실행되어도 충돌 ❌
완료 후 메인으로 *머지*
```

`git worktree` 표준 기능 활용. Anthropic agent SDK 의 `Agent` tool 도 `isolation: "worktree"` 옵션 지원.

## 5. `/harness` 가 작동할 때 — 살아있는 C+C+S 사례

추상 이론이 아니라 *실제로 이 강의 레포에서 도는* C+C+S 사례. 세 장면으로 분해해 본다.

### 장면 ① — `/harness` 5단계 흐름 (Control 측면)

```text
1️⃣  [자동]   docs/ 문서를 전부 읽는다           ← State 로드
            (PRD · ARCHITECTURE · ADR · UI_GUIDE)

2️⃣  [같이]   사용자와 논의                     ← Human-in-the-Loop
            (구체화할 게 있으면 묻는다)

3️⃣  [자동]   구현 계획을 Phase 로 쪼갠다        ← Control: 분할
4️⃣  [자동]   Phase 파일 생성 (phases/{task}/)  ← State: 영속화
5️⃣  [자동]   execute.py 실행                  ← Control: 순차 스케줄
```

**5 단계 중 *4 단계가 자동*** — 사람이 끼어드는 건 2번 한 번뿐. 그것도 *"AI가 이해를 못 해서"* 가 아니라 *"방향을 같이 정하기 위해"*. [HITL](../../concepts/Human-in-the-Loop.md) 의 *결정적 체크포인트* 가 정확히 한 곳에 박힌 사례.

### 장면 ② — `execute.py` 실행 결과 (State + Contracts 측면)

```text
$ python3 scripts/execute.py mvp

============================================
 Harness Executor
 Task: mvp  |  Phases: 5  |  Pending: 5
============================================

 ✓ Phase 1: 프로젝트-초기화        [180s]   ← 각 Phase = Contract 통과
 ✓ Phase 2: 타입-+-유틸리티        [300s]
 ✓ Phase 3: api-라우트             [240s]
 ✓ Phase 4: ui-컴포넌트            [300s]
 ✓ Phase 5: 메인-페이지-통합       [150s]

============================================
 Task 'mvp' completed!  ← Stop 조건: 5/5 + 통합 테스트
============================================

⏱  17분 — 총 소요 시간
✅  5/5 — Phase 완료
🧪  54개 — 테스트 통과
```

여기서 *각 Phase 의 ✓ 는 Contract* 다. *코드 완성 + 테스트 통과 + 자동 커밋* 이라는 *3 게이트* 를 다 넘어야 ✓ 가 찍힌다. 한 게이트라도 실패하면 — 자동 재시도, 그래도 실패면 *사람 호출*.

### 장면 ③ — `claude -p` 헤드리스 + *무기억* 사이클 (State 영속화의 진짜 이유)

```text
 Phase 1   →   Phase 2   →   Phase 3   →   Phase 4   →   Phase 5
 claude -p    claude -p     claude -p     claude -p     claude -p
   #1           #2            #3            #4            #5
              ✗ 기억 없음   ✗ 기억 없음   ✗ 기억 없음   ✗ 기억 없음
```

각 Phase 가 *완전히 새로운 Claude*. **이전 Phase 기억이 없다.** *Phase 5 가 Phase 1 의 결정을 알 수 있는 유일한 길은 — *문서로 남아 있는 것* 뿐*.

이게 *왜 docs/ 가 그렇게 중요한가* 의 진짜 이유다.

> **하니스의 진짜 역할은 — AI가 매번 잊어버리는 만큼, *매번 다시 알려줄 수 있는 기록 시스템* 을 만들어주는 것.**

C+C+S 정의 중 *State 영속화* 가 *이론적 우아함* 이 아니라 *실전 필수* 인 이유 — `claude -p` 의 무기억 매커니즘이 그걸 *강제* 하기 때문.

**자세한 헤드리스 모드 작동 방식**: [Claude Code Headless 모드](../../tools/Claude-Code-Headless-모드.md).

## 한계

- **C+C+S 설계 자체의 비용**: 큰 작업에서 *Phase 어떻게 쪼갤지* 결정이 어려움. → `/harness` 같은 메타 도구가 자동화.
- **상태 폭증**: 7폴더에 매번 보고서 쌓이면 — 시간이 지나며 *오래된 정보가 새 결정을 오염*. 정기 정리 필요.
- **종료 기준 모호**: *"언제 끝났다고 할까"* 가 가장 어렵다. 무한 루프 위험. 최대 시도 횟수 + 사람 종료 권한 필수.

## 꼬리에 꼬리 (관련 개념)

- [하니스 엔지니어링](../하니스-엔지니어링.md) — 부모 문서
- [Orchestration](../Orchestration.md) — Control 의 *상위 추상화*
- [Tools](tools.md) — Phase 안에서 호출되는 도구들
- [서브에이전트와 분업](subagents-and-delegation.md) — Phase 별로 다른 서브에이전트 위임
- [Evaluation Loop](evaluation-loop.md) — Gate 의 *검증* 매커니즘
- [퍼미션·훅](permissions-and-hooks.md) — Stop hook 으로 *조건부 종료*
- [하이퍼-워터폴](../../methodologies/하이퍼-워터폴.md) — C+C+S 의 *방법론적 구현*
- [문서 주도 개발](../문서-주도-개발.md) — State 영속화의 *문서적 표준*
- [Claude Code Headless 모드](../../tools/Claude-Code-Headless-모드.md) — Phase 별 무기억 호출의 매커니즘

## 출처

- [Anthropic — Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Control 디자인
- [LangChain — The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) — C+C+S 정의
- [Anthropic Cookbook — Worktree isolation patterns](https://github.com/anthropics/anthropic-cookbook) — 격리 패턴
- [hyper-waterfall — rhwp 매뉴얼 (edwardkim)](https://github.com/edwardkim/rhwp/blob/main/mydocs/manual/hyper_waterfall.md) — 7폴더 사례
