# Claude Code 헤드리스 모드 (`claude -p`)

> 사람이 채팅창 앞에 앉아 있지 않고 — *스크립트가 프로그래밍적으로 Claude를 실행*하는 모드. 하니스 자동화의 핵심 매커니즘. **`execute.py` 가 5단계를 사람 없이 흘릴 수 있는 이유**.

## 1. 왜 "헤드리스(Headless)"라고 부르나

- **Headless**: 컴퓨팅에서 *"화면(=머리)이 없는"* 모드를 가리키는 표준 용어. 헤드리스 브라우저(Headless Chrome)·헤드리스 CMS 등에서 같은 의미로 쓰인다.
- 사용자 인터랙션 없이 *프로그램이 프로그램을 호출하는* 방식.
- Claude Code에서는 **`claude -p`** (또는 `--print`) 플래그로 호출. 과거에는 *"headless mode"*라고 명명됐다가 현재 공식 문서는 `-p` 플래그를 표준 용어로 사용.

## 2. 그전에는 어떤 문제가 있었나

대화형 LLM 도구(ChatGPT 웹·Claude Code 인터랙티브 모드)는 *사람이 매 턴마다 입력*하는 구조였다.

- 자동화 파이프라인에 끼우기 어렵다 — *사람의 키보드 입력*이 필요한 명령은 스크립트가 호출할 수 없음
- 100개의 PR을 일괄 리뷰? 사람이 100번 채팅창을 열어야 함
- CI/CD에 통합 불가 — GitHub Actions가 사람을 깨워 키보드 앞에 앉힐 수는 없음
- 야간 작업·정기 점검 같은 *"사람 없이 굴러야 하는 일"* 에 LLM을 못 쓴다

**일상 비유**: 키오스크는 손님이 *직접 화면을 누르는* 식이고, 자판기는 *동전만 넣으면 작동*. 둘 다 같은 "주문 → 발급" 흐름이지만, 자판기는 *사람의 손가락 누름이 필요 없다*. `claude -p`는 Claude를 *자판기처럼 부를 수 있게* 만든 모드.

## 3. 어떻게 해결했나

Claude를 표준 *명령줄 도구*로 만든 것. stdin·stdout·exit code를 가진 일반 CLI 도구처럼 동작 — 즉 *파이프·리다이렉트·CI*에 그대로 끼워 쓸 수 있다.

### 기본 사용법

```bash
$ claude -p "Find and fix the bug in auth.py" \
    --allowedTools "Read,Edit,Bash"
[프롬프트 → 작업 수행 → stdout 출력 → 종료]
```

### 핵심 특성

- **stdin 읽기 가능** — `cat code.py | claude -p "리뷰해줘"` 식으로 파이프
- **JSON 출력 옵션** — `--output-format json` 추가 시 `total_cost_usd` 등 메타데이터 포함 wrapper로 반환
- **도구 화이트리스트** — `--allowedTools` 로 사용 가능 도구 제한 (1층 도구 경계 보강)
- **종료 후 끝** — 각 호출은 *완전히 새로운 세션*. 이전 호출의 기억이 없다

## Before/After — 같은 작업, 두 모드 비교

```text
[대화형 모드]                       [헤드리스 모드]
  $ claude                            $ claude -p "리뷰" \
  > 이 PR 리뷰해줘                       --output-format json
  > 보안 관점도 봐줘                     > review.json
  > JSON으로 정리해줘                    [한 줄로 끝]
  ...
  사람이 매 턴 입력                    스크립트에서 한 번 호출
  세션 동안 기억 유지                  매 호출은 무기억(stateless)
```

## 강의 연결 포인트 — `execute.py` 매커니즘

**`/harness` 흐름과 `claude -p` 매커니즘 콤보 슬라이드**가 정확히 이 모드를 설명한다.

```text
Phase 1   →   Phase 2   →   Phase 3   →   Phase 4   →   Phase 5
claude -p     claude -p     claude -p     claude -p     claude -p
   #1            #2            #3            #4            #5
              ✗ 기억 없음   ✗ 기억 없음   ✗ 기억 없음   ✗ 기억 없음
```

여기서 **재미있는 점** — 각 Phase는 *완전히 새로운 Claude*. 이전 Phase의 기억이 없다.

> 그래서 docs/ 에 *전부* 적어두는 게 중요하다. Phase 5가 Phase 1의 결정을 알 수 있는 *유일한 길*은, **문서로 남아 있는 것**뿐이다.

이게 *"하니스의 모든 요소는 모델이 혼자서는 못 하는 일에 대한 가정을 코드화한 것"* 정의의 가장 진한 사례. **AI가 매번 잊어버리는 만큼, 우리가 *매번 다시 알려줄 수 있는 기록 시스템*을 만든다**.

## 라이브 시연 가능한 예시

### 시연 1 — 헤드리스로 PR 리뷰
```bash
$ claude -p "Review this PR for security issues" \
    --output-format json > analysis.json
$ cat analysis.json | jq '.cost'
0.142
```
청중에게: *"이 한 줄로 사람 손 안 거치고 보안 리뷰 + 비용까지 자동 추적이 끝났다"*.

### 시연 2 — 무기억 입증
```bash
$ claude -p "내 이름은 영철이야"
"네, 영철님 반갑습니다."

$ claude -p "내 이름이 뭐였더라?"
"이전 대화 기록을 가지고 있지 않아 답변하기 어렵습니다."
```
같은 사람이 같은 터미널에서 호출했는데도 — *완전히 새로운 세션*. **무기억의 라이브 증거**.

## 실제 사용 사례

- **CI/CD**: GitHub Actions에서 PR 자동 리뷰 (`claude -p "Review" > comment.md`)
- **배치 작업**: 100개 파일에 대해 *for-loop*으로 동일 처리
- **야간 자동화**: cron으로 매일 새벽에 코드베이스 헬스체크
- **이번 강의의 `execute.py`**: Phase 파일을 순회하며 5번 `claude -p` 호출, 각 단계마다 자동 커밋

## 꼬리에 꼬리 (관련 개념)

- [Claude Code](Claude-Code.md) — 헤드리스 모드의 호스트
- [Claude-Code 1층 하니스](Claude-Code-1층-하니스.md) — 헤드리스에서도 1층은 그대로 작동
- [Claude Code Hooks](Claude-Code-Hooks.md) — 헤드리스 호출도 모든 hook 이벤트가 발화
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — *무기억* 한계 때문에 docs/에 모든 컨텍스트를 남기는 이유
- [Claude Code 세션 운영](Claude-Code-세션운영.md) — 헤드리스 = *1회용 세션* 으로서 영속 컨텍스트 오염을 원천 차단하는 패턴

## 출처

- [Anthropic — Run Claude Code programmatically (Claude Code Docs)](https://code.claude.com/docs/en/headless) — 공식 명세
- [Claude Code Headless Mode (cld-docs.onlinetool.cc)](https://cld-docs.onlinetool.cc/en/docs/claude-code/headless.html) — 사용 패턴 정리
- [MindStudio: What Is Claude Code Headless Mode?](https://www.mindstudio.ai/blog/claude-code-headless-mode-autonomous-agents) — 자율 에이전트 활용 사례
- [Angelo Lima: CI/CD and Headless Mode with Claude Code](https://angelo-lima.fr/en/claude-code-cicd-headless-en/) — GitHub Actions 통합
