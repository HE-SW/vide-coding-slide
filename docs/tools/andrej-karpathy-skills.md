# andrej-karpathy-skills

> Andrej Karpathy의 *"Claude Code를 몇 주 써본 관찰"* 트윗(2026-01-26)을 한 장의 [CLAUDE.md](CLAUDE-md.md)로 압축한 오픈소스 프로젝트. 작성자 **Forrest Chang**(`forrestchang`)이 2026-01-27 GitHub에 공개, 약 3개월 만에 **10만 ★ 돌파** — GitHub 역사상 가장 빨리 별을 모은 레포 중 하나로 회자됨.

## 1. 한 줄 정의

- 단 한 장의 `CLAUDE.md`(약 65줄)로 구성된 **AI 코딩 행동 가이드라인 템플릿**
- Karpathy가 지적한 LLM 코딩의 4대 실패 패턴을 **4가지 원칙**으로 변환
- Claude Code 플러그인(`/plugin install andrej-karpathy-skills@karpathy-skills`)으로도 제공, Cursor 룰 파일도 동봉
- 라이선스 MIT, 어떤 프로젝트의 기존 CLAUDE.md에든 합쳐 쓸 수 있도록 설계됨

## 2. 그전에는 어떤 문제가 있었나 — Karpathy의 관찰

2026년 1월 말, Karpathy는 X에 *Claude Code를 집중적으로 쓰며 정리한 메모*를 올렸다. 한 줄 요약: **"모델은 똑똑하지만, 작업자로서는 게으른 신입사원처럼 군다"**.

그가 짚은 4가지 실패 패턴:

1. **잘못된 가정을 말없이 굳히고 그대로 달려간다** — 확인하지 않음, 혼란을 드러내지 않음, 트레이드오프를 제시하지 않음, 반박하지 않음
2. **코드와 API를 지나치게 부풀린다** — 100줄이면 될 일을 1,000줄로, 불필요한 추상화를 양산
3. **건드리지 말라는 코드를 부수적으로 손댄다** — 작업과 무관한 주석·죽은 코드까지 임의로 수정·삭제
4. **검증 가능한 성공 기준 없이 "완료"를 선언한다** — *"LLM은 명확한 목표가 있으면 스스로 잘 루프 돈다. 명령하지 말고 성공 기준을 줘라."*

이 트윗 한 편이 *"왜 내 Claude는 시키지도 않은 걸 자꾸 하지?"* 라는 전 세계 개발자의 묵은 답답함을 정확히 말로 옮겨준 셈. 조회수가 폭발적으로 올랐다.

## 3. andrej-karpathy-skills가 어떻게 해결했나

Forrest Chang은 트윗을 읽고 **"규율을 일일이 지시하지 말고 한 장의 파일로 못 박자"** 는 발상으로, 4대 실패 패턴 → 4대 원칙으로 1:1 매핑한 CLAUDE.md를 공개했다.

### 4가지 원칙 (정확한 번역)

| # | 원칙 | 핵심 한 줄 | 어떤 실패를 막나 |
|---|---|---|---|
| 1 | **Think Before Coding** (코딩 전 사고) | 가정하지 마라, 혼란을 숨기지 마라, 트레이드오프를 드러내라 | 잘못된 가정·암묵적 결정 |
| 2 | **Simplicity First** (단순함 우선) | 문제를 푸는 최소 코드만, 추측성 기능 없이 | 과잉 추상화·코드 부풀림 |
| 3 | **Surgical Changes** (외과 수술적 수정) | 꼭 필요한 곳만 만져라, 네가 만든 잔해만 청소해라 | 무관한 코드 임의 수정 |
| 4 | **Goal-Driven Execution** (목표 주도 실행) | 검증 가능한 성공 기준을 정의하고 그 기준에 닿을 때까지 루프해라 | 모호한 "완료" 선언 |

### 4번 원칙의 실전 변환 예시

| ❌ 명령형 | ✅ 목표형 |
|---|---|
| "validation 추가해줘" | "잘못된 입력에 대한 테스트를 먼저 짜고, 그걸 통과시키도록 해줘" |
| "버그 고쳐줘" | "버그를 재현하는 테스트부터 짜고, 그걸 통과시켜라" |
| "X 리팩터링해줘" | "리팩터링 전후로 모든 테스트가 통과해야 한다" |

→ Karpathy 인용: *"LLMs are exceptionally good at looping until they meet specific goals. Don't tell it what to do, give it success criteria and watch it go."*

### 설치 방법 (2가지)

**A. Claude Code 플러그인 (권장)**
```
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```
→ 모든 프로젝트에 전역으로 적용. 개별 CLAUDE.md를 만지지 않아도 됨.

**B. 프로젝트별 CLAUDE.md에 합치기**
```bash
# 새 프로젝트
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md

# 기존 프로젝트에 이어붙이기
echo "" >> CLAUDE.md
curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
```

Cursor 사용자를 위해 `.cursor/rules/karpathy-guidelines.mdc`도 동봉.

## 4. 강의 연결 포인트 (1·2강)

- **1강 [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md)**: *"좋은 답변은 좋은 컨텍스트에서 나온다"* 메시지의 가장 강력한 사례. **65줄짜리 텍스트 한 장**이 같은 모델의 행동을 통째로 바꾼다 — 모델 학습이나 파인튜닝 없이 **컨텍스트만 갈아끼워서**.
- **2강 [CLAUDE.md](CLAUDE-md.md)**: 기본 CLAUDE.md 작성법을 가르친 직후, *"이미 잘 정리된 한 장이 있으니 가져다 써도 된다"* 는 사례로 자연스럽게 연결. 2층(프로젝트 CLAUDE.md) 위에 얹는 보편 규율 레이어로 소개 가능.
- **["Surgical Changes" 원칙**은 2강의 [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) 슬라이드와 직결: *"AI가 시키지도 않은 걸 건드리는 것"* 이 바로 강의자가 청중에게 보여주려는 가장 흔한 실패 시연 장면.

## 5. 한계와 주의

- **만능 아님**: 작성자 본인도 *"trivial한 작업(오타 수정 등)에는 풀 규율이 과하다. 판단해서 써라"* 고 명시. 속도 vs. 신중함의 트레이드오프가 있다.
- **Karpathy 본인 작품 아님**: 종종 *"카파시가 만든 CLAUDE.md"* 로 잘못 인용된다. 실제로는 카파시 트윗을 **Forrest Chang이 해석·재구성**한 2차 저작물. 강의에서 인용할 때 출처를 정확히 말할 것.
- **프로젝트별 규칙은 별도**: 4원칙은 *행동* 가이드일 뿐, 스택·컨벤션은 사용자가 자기 프로젝트의 CLAUDE.md에 따로 추가해야 한다.

## 꼬리에 꼬리 (관련 개념)

- [Andrej Karpathy](../people/Andrej-Karpathy.md) — 4대 실패 패턴을 처음 명시화한 원저자
- [CLAUDE.md](CLAUDE-md.md) — 이 프로젝트가 사용하는 그릇
- [Claude Code](Claude-Code.md) — 플러그인이 동작하는 무대
- [컨텍스트 엔지니어링](../techniques/컨텍스트-엔지니어링.md) — 상위 개념 (텍스트 한 장으로 행동을 바꾸는 사례)
- [하니스 엔지니어링](../techniques/하니스-엔지니어링.md) — "Goal-Driven Execution" 원칙이 직접 연결
- [oh-my-claudecode (OMC)](oh-my-claudecode.md) — Claude Code 위에 얹는 다른 형태의 외부 레이어 (멀티 에이전트)

## 출처

- [forrestchang/andrej-karpathy-skills (GitHub)](https://github.com/forrestchang/andrej-karpathy-skills) — 1차 출처. 2026-01-27 공개, MIT 라이선스, 2026-05 기준 약 11.6만 ★
- [Karpathy 원본 트윗 (2026-01-26)](https://x.com/karpathy/status/2015883857489522876) — 4대 실패 패턴이 처음 언급된 게시물
- [Karpathy's CLAUDE.md: The 65-Line File With 100K GitHub Stars (Miraflow, 2026)](https://miraflow.ai/blog/karpathy-claude-md-100k-github-stars-ai-coding-2026) — 배경·반응 정리
- [Karpathy Skills: The LLM Coding Manifesto (BrightCoding, 2026-04-29)](https://www.blog.brightcoding.dev/2026/04/29/karpathy-skills-the-revolutionary-llm-coding-manifesto) — 4원칙 해설
- [Turning Andrej Karpathy's LLM Coding Thoughts into Claude.md (Substack)](https://todatabeyond.substack.com/p/turning-andrej-karpathys-llm-coding) — Forrest Chang의 변환 의도 분석
- [Former Tesla AI chief Andrej Karpathy now codes "mostly in English" (the-decoder)](https://the-decoder.com/former-tesla-ai-chief-andrej-karpathy-now-codes-mostly-in-english-just-three-months-after-calling-ai-agents-useless/) — 카파시의 LLM 코딩 입장 변화 맥락
