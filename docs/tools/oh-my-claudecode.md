# oh-my-claudecode (OMC)

> **2026-05-07 기준, v4.13.6 / GitHub 32.7k★ / MIT 라이선스.**
> Claude Code 위에 얹는 멀티 에이전트 오케스트레이션 플러그인. "Claude Code를 배우지 마세요. 그냥 OMC를 쓰세요"가 공식 슬로건.

---

## 1. 왜 "oh-my-claudecode"라고 부르나

- **만든 사람**: Yeachan Heo (허예찬, GitHub `@Yeachan-Heo`). 본업은 퀀트 트레이딩, 사이드 프로젝트로 멀티 에이전트 오케스트레이션 시스템을 다룬다.
- **이름의 계보**: 1992년 등장한 zsh 설정 프레임워크 **oh-my-zsh** ("그냥 깔면 기본기가 다 갖춰진 셸 환경") → 2025년 등장한 **oh-my-opencode**(OpenCode용 멀티 에이전트 프리셋) → 그 흐름을 Claude Code에 가져온 것이 **oh-my-claudecode**다. "별로 안 만져도 일단 강해지는 기본 세팅"이라는 함의.
- **npm 패키지명**: `oh-my-claude-sisyphus`. **시지프스(Sisyphus) 신화**를 비유로 가져옴 — "끝까지 굴려 올린다"는 자동화/반복 루프 철학을 담음. 작업이 검증될 때까지 멈추지 않는다.
- **공식 태그라인**: *"A weapon, not a tool"* (도구가 아니라 무기) / *"학습 곡선 제로. 최대 파워."*

## 2. 그전에는 어떤 문제가 있었나

Claude Code 자체는 강력하지만, **잠재력의 대부분은 사용자가 직접 조립해야 풀린다.** 강의에서 다룬 "하니스 엔지니어링" 관점에서 보면, Claude Code는 **하니스를 만들 수 있는 도구**일 뿐, 하니스 자체가 아니다.

비개발자 청중용 비유:
> Claude Code가 **공구함**이라면, 거기엔 망치·드라이버·드릴이 다 들어있다. 그런데 "집을 지어라"고 하면, 어느 공구를 언제 쓸지, 일꾼을 몇 명 부를지, 누가 무슨 일을 할지를 **사용자가 직접 지휘**해야 한다.

구체적으로 vanilla Claude Code의 한계:

- **단일 모델 한계** — Claude만 쓰게 되어 있다. Gemini의 1M 컨텍스트, Codex의 코드 검증 같은 다른 모델의 강점을 같이 쓰려면 직접 붙여야 함.
- **수동 작업 분해** — "이 일은 분석에 강한 모델로, 저 일은 빠른 모델로"를 사용자가 매번 골라줘야 함.
- **병렬성 부족** — 기본은 순차 실행. 큰 리팩터링을 동시에 여러 가닥으로 돌리려면 직접 설계해야 함.
- **세션 간 기억 약함** — `CLAUDE.md` 외에는 프로젝트별 영속 메모리/노트패드가 빈약.

그 결과: **"파워 유저만 Claude Code를 제대로 쓴다"** 라는 격차가 생긴다.

## 3. 어떻게 해결했나

OMC는 Claude Code의 **플러그인**으로 들어가, 위 4가지를 한꺼번에 메운다.

### (1) 5가지 실행 모드 — 사용자는 모드만 고른다

| 모드 | 용도 | 한 줄 설명 |
|---|---|---|
| **Team** (권장) | 표준 파이프라인 | `plan → PRD → execute → verify → fix` 단계별 멀티 에이전트 |
| **Autopilot** | 풀 자율 | "기능 X 만들어줘" 한 줄 → 테스트까지 끝낸 코드 산출 |
| **Ralph** | 끈질긴 검증 루프 | 아키텍트가 "완료"라고 할 때까지 자가 반복 |
| **Ultrawork** | 최대 병렬 | 여러 수정/리팩터링을 동시에 굴림 |
| **Pipeline** | 순서 보존 | 엄격한 순서가 필요한 다단계 작업 |

추가로 `/deep-interview`는 **소크라테스식 질문**으로 모호한 요구사항을 명확하게 만들어준다. "뭘 만들고 싶은지 모르겠을 때" 코드 짜기 전에 던지면 가장 좋은 입구.

### (2) 19개 전문 에이전트 + 36개 스킬

아키텍처/리서치/디자인/테스트/데이터 사이언스 등 도메인별로 전문 에이전트가 미리 박혀 있다. 사용자가 매번 "너는 아키텍트 역할이야"라고 시키지 않아도 적절한 에이전트로 자동 위임된다.

### (3) 자동 모델 라우팅

작업 복잡도에 따라 **Haiku (빠름) / Sonnet (표준) / Opus (추론)** 를 자동 선택한다. 단순 조회는 Haiku, 아키텍처 결정은 Opus.

### (4) 멀티 모델 협업 (선택)

`tmux` 위에서 Codex CLI, Gemini CLI를 워커로 띄워 **교차 검증**. 디자인 리뷰는 Gemini, 코드 검증은 Codex 식으로 분담.

### (5) 영속 상태

- `.omc/skills/` (프로젝트, git 공유)
- `~/.omc/skills/` (개인, 프로젝트 간 공유)
- 세션 간 노트패드, 프로젝트 메모리

### 설치

```bash
# 권장: Claude Code 마켓플레이스
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode

# 또는 npm
npm i -g oh-my-claude-sisyphus@latest
```

**필수**: Claude Code CLI + Max/Pro 구독 (또는 API 키)
**권장**: `tmux` (멀티 모델/병렬 모드용)

---

## 강의 연결 포인트

강의의 **하니스 엔지니어링** 섹션에서 "프롬프트 → 컨텍스트 → 하니스" 단계 진화의 **현재 도착점** 사례로 OMC를 짧게 소개하면 자연스럽다.

> *"Claude Code가 공구함이라면, oh-my-claudecode는 그 공구함에 '미리 짜둔 작업조'를 한꺼번에 부르는 단축 버튼을 단 거예요. 강의에서 본 '하니스를 만든다'는 일을 누군가가 대신 해서 깃허브에 풀어놓은 셈입니다. 별 3만 개가 그 가치에 대한 시장의 답이고요."*

청중에게 줄 메시지:
- **"바이브코딩은 이미 1세대를 지나 2세대로 가고 있다"** — 단순히 LLM에 부탁하는 단계에서, **LLM 여러 명을 어떻게 협업시키는가**로 관심이 옮겨가는 중.
- **"오픈소스로도 이런 게 가능하다"** — Anthropic이 만들지 않아도 커뮤니티가 만든다. 비개발자가 이름은 몰라도 이런 흐름이 있다는 인식만 남기면 충분.

⚠️ **주의**: 강의에서 "이거 깔고 따라 해보세요"라고 시연하지는 말 것. OMC는 파워 유저용이고, 비개발자가 직접 설치하면 오히려 압도된다. **"이런 게 있다"**까지만.

---

## 꼬리에 꼬리 (관련 개념)

- [Claude Code](Claude-Code.md) — OMC가 얹히는 베이스. `/plugin` 명령어로 OMC 같은 플러그인을 설치한다.
- [Claude Code Plugin](Claude-Code-Plugin.md) / [Plugin Marketplace](Plugin-Marketplace.md) — OMC가 *플러그인 형태로 유통될 때* 거치는 묶음 단위와 카탈로그 레이어.
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — OMC는 "남이 미리 만들어둔 하니스 패키지"로 볼 수 있다.
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — 영속 노트패드/프로젝트 메모리는 컨텍스트 관리 자동화의 한 형태.
- [Andrej Karpathy](../people/Andrej-Karpathy.md) — "바이브코딩"·"컨텍스트 엔지니어링"이라는 용어를 정착시킨 인물. OMC 같은 도구가 그 흐름의 산물.

---

## 출처

- 공식 저장소: https://github.com/Yeachan-Heo/oh-my-claudecode
- 공식 사이트: https://oh-my-claudecode.dev/
- 한국어 README: https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/README.ko.md
- npm 패키지: https://www.npmjs.com/package/oh-my-claude-sisyphus
- 레퍼런스 문서: https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/docs/REFERENCE.md
- 만든 사람 GitHub: https://github.com/Yeachan-Heo (Bellman)

> ⚠️ OMC는 매우 빠르게 업데이트된다 (2026-05-07 기준 224개 릴리스, v4.13.6). 강의 직전에 GitHub 릴리스 페이지에서 최신 모드/명령어 명을 한 번 더 확인할 것.
