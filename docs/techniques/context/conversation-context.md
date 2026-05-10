# Conversation Context (대화 컨텍스트)

> 사용자가 *지금 이 순간* 던지는 메시지 + *이전 턴들의 누적*. 컨텍스트 엔지니어링의 *흘러가는 강물*. **메모리**(단기·장기)가 같이 산다.

> 부모 문서: [컨텍스트 엔지니어링](../컨텍스트-엔지니어링.md)

## 1. 정의

Conversation context는 **현재 대화 안에서 모델이 보는 모든 사용자-어시스턴트 턴**이다.

세 부분:
- **현재 사용자 메시지** (Query) — *지금 막 도착한 입력*
- **대화 히스토리** (History) — 같은 세션의 이전 턴들
- **메모리** (Memory) — 세션을 넘어 *지속*되는 지식

## 2. 그전에는 어떤 문제가 있었나

LLM은 *세션마다 새로운 사람*이다. 같은 사용자가 어제 한 말을 오늘은 모른다.

- *"지난번에 말한 거 기억나?"* → 모름
- *내 이름·선호·과거 결정* 을 매번 다시 알려줘야 함
- 긴 대화 안에서도 — 컨텍스트 창이 차면 *앞 내용이 잘려나감*

→ 모델에 *대화 흐름을 유지하는 매커니즘*이 필요했다.

**일상 비유**: 매일 만나는 친구가 *나를 기억한다*. 의사·변호사도 *나의 차트·기록*을 본다. 그러나 LLM은 기본적으로 *처음 만난 사람*. 메모리·히스토리가 그 *친구 관계*를 만든다.

## 3. 구조 — 두 종류의 메모리

### (A) 단기 메모리 (Short-Term / Conversational Memory)

같은 세션 안의 이전 턴 보존. 컨텍스트 창에 그대로 누적.

```text
[Turn 1]
USER: "내 이름은 영철이야"
AI:   "영철님 반갑습니다."

[Turn 2]
USER: "내 이름이 뭐였지?"
AI:   "영철님이라고 말씀하셨습니다."   ← 단기 메모리 작동
```

문제: 대화가 길어지면 — 컨텍스트 창 한계로 *앞 턴이 잘려나감*. → `/compact` 같은 *대화 요약* 기능으로 보완.

### (B) 장기 메모리 (Long-Term / Persistent Memory)

세션을 넘어 *영속*되는 지식. 외부 저장소에 보관 후 — 새 세션에서 자동 주입.

```text
[Day 1, Session 1]
USER: "내 이름은 영철이야"
AI:   [저장소에 저장]

[Day 5, Session 17]
USER: "안녕"
AI:   "영철님, 5일 만이네요."   ← 장기 메모리 작동
```

**구현 방식 (2026)**:
- **Claude Code의 자동 메모리** — 세션마다 자동 저장·다음 세션에서 검색·주입
- **CLAUDE.md** — *수동* 장기 메모리 (사용자가 적어두는 사실들)
- **벡터 DB / 임베딩 검색** — 검색형 장기 메모리. *"관련 있는 과거 기록만"* 가져옴

## Before / After

```text
[BEFORE — 메모리 없음]
Day 1 USER: "나는 비건이야. 음식 추천 시 고려해줘"
Day 1 AI:   "알겠습니다."

Day 2 USER: "저녁 메뉴 추천해줘"
Day 2 AI:   "삼겹살 어떠세요?"
            (= 어제 비건이라고 한 거 잊음)

[AFTER — 장기 메모리]
Day 1 USER: "나는 비건이야"
Day 1 AI:   [장기 메모리에 *식이 제한: vegan* 저장]

Day 2 USER: "저녁 메뉴 추천해줘"
Day 2 AI:   "두부 카츠동 어떠세요? 비건 옵션입니다."
```

## 라이브 시연 가능한 예시

### 시연 1 — 단기 메모리 (`/compact` 효과)
```bash
[강의 중 — 50번째 turn]
USER: "처음에 우리가 정한 코딩 스타일이 뭐였지?"
AI:   "음... 정확한 기록이 없어 답변하기 어렵습니다"
       (= 컨텍스트 창에서 잘림)

[/compact 실행 후]
USER: "처음에 우리가 정한 코딩 스타일이 뭐였지?"
AI:   "들여쓰기 2칸 + camelCase 함수명을 정하셨습니다."
       (= 요약이 컨텍스트로 다시 들어옴)
```

### 시연 2 — 장기 메모리
```bash
[Session A]
USER: "나는 매주 월요일 1on1 미팅 노트를 쓰는데, 항상 같은 양식이야: 안건/논의/액션"
AI:   [저장소에 양식 저장]

[Session B (며칠 후, 새 세션)]
USER: "1on1 노트 시작"
AI:   "## 안건
       ## 논의
       ## 액션"  (= 저장된 양식 자동 적용)
```

## 4. 실제 사례 (2026 기준)

- **ChatGPT Memory** (2024-04 출시): GUI로 *기억 관리*. *"내 직업은 데이터 사이언티스트"* 같은 사실을 자동 저장.
- **Claude Code Memory** (2026): `~/.claude/projects/{프로젝트}/memory/` 에 마크다운 파일들로 영속. 자동 갱신.
- **Cursor / Windsurf**: 워크스페이스 메모리 표준 채택.
- **Mem0, Zep** 같은 *외부 메모리 서비스*: 여러 LLM에서 공통 메모리 사용.

## 한계와 주의

- **잘못된 기억의 누적**: AI가 잘못 기억한 사실이 *영구 박힘* — 정기적으로 검토 필요.
- **프라이버시**: 어떤 사실이 *어디에* 저장되는지 사용자가 제어해야 함. 비밀번호·민감 정보 자동 저장 ❌.
- **메모리 의존**: 모델이 *기억* 으로만 답하지 않게 — 중요한 결정은 매번 사용자가 *명시적 지시*.

## 꼬리에 꼬리 (관련 개념)

- [컨텍스트 엔지니어링](../컨텍스트-엔지니어링.md) — 부모 문서
- [System Context](system-context.md) — 안쪽 레이어
- [Knowledge Context](knowledge-context.md) — 외부 자료 측
- [Tool & Environment Context](tool-environment-context.md) — 도구 결과 측
- [CLAUDE.md](../../tools/CLAUDE-md.md) — 수동 장기 메모리의 표준
- [Lost in the Middle](../../phenomena/Lost-in-the-Middle.md) — 대화가 길어질 때 메모리가 묻히는 이유

## 출처

- [Anthropic — Conversation memory best practices](https://platform.claude.com/docs/build-with-claude/conversational-memory) — 공식 패턴
- [DailyDoseofDS — Memory and Temporal Context](https://www.dailydoseofds.com/llmops-crash-course-part-8/) — 메모리 분류
- [Mem0 — Memory Layer for AI Agents](https://mem0.ai/) — 외부 메모리 표준 사례
- [Zep — Long-term memory for AI agents](https://www.getzep.com/) — temporal knowledge graph 메모리
