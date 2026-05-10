# Knowledge Context (지식 컨텍스트)

> 모델이 *학습한 적 없는 정보*를 답할 수 있도록 — *외부 문서·데이터베이스·웹*에서 가져와 컨텍스트에 주입하는 영역. **RAG가 사는 자리**. 환각의 가장 강력한 해독제.

> 부모 문서: [컨텍스트 엔지니어링](../컨텍스트-엔지니어링.md)

## 1. 정의

Knowledge context는 **모델 가중치에 *없는* 정보를 응답 직전에 *주입*하는** 컨텍스트 레이어다.

대표 출처:
- 회사 내부 문서 (위키·정책·코드베이스)
- 사용자 개인 자료 (노트·이메일)
- 실시간 웹 검색 결과
- 데이터베이스 쿼리 결과
- 학술 논문·법률 자료

## 2. 그전에는 어떤 문제가 있었나

LLM은 *학습 컷오프* 이후 정보를 모른다 (자세히는 [Knowledge Cutoff](../../phenomena/Knowledge-Cutoff.md)).

- *"우리 회사 휴가 정책 알려줘"* → 모델은 회사 문서를 본 적 없음
- *"오늘 날씨"* → 학습 시점 이후 정보 없음
- *"이 PDF 요약해줘"* → 첨부 파일 없으면 답 불가

→ 모델 *바깥*에서 정보를 가져와 *주입*하는 표준 패턴이 필요했다.

**일상 비유**: 시험 보는 학생이 *책을 펴 놓고 답하기*. 모르는 걸 외우려 하지 않고 — *가져다 보면서 답함*. RAG가 그 *오픈북 시험* 매커니즘.

## 3. 어떻게 작동하나 — 5단계

```text
1. 사용자 질문                         "회사 휴가 정책은?"
   ↓
2. 검색 (Retrieval)                    회사 위키에서 관련 페이지 찾기
                                       └─ 보통 *벡터 검색* (의미 기반)
   ↓
3. 컨텍스트 주입                       찾은 문서 내용을 프롬프트에 추가
   ↓
4. 생성 (Generation)                   LLM이 *문서를 보면서* 답을 만듦
   ↓
5. (선택) 출처 표기                    "출처: 휴가 규정 §3.2"
```

→ 자세히는 [RAG](../RAG.md) 문서.

### 두 가지 큰 전략

**(A) 미리 인덱싱 (Pre-indexed RAG)**
- 회사 위키 전체를 미리 *벡터 DB*에 저장
- 사용자 질문이 오면 *유사도 검색*으로 관련 페이지 찾아 주입
- 가장 흔한 형태

**(B) 실시간 검색 (Live Retrieval)**
- 매 질문마다 *웹 검색* 또는 *API 호출*
- Perplexity, ChatGPT Browse, Claude Web Search 가 이 패턴
- 최신성 보장, 그러나 매번 검색 비용

## Before / After

```text
[BEFORE — Knowledge context 없음]
USER: "우리 회사 환불 기간은?"
AI:   "일반적으로 7~30일 정도..."  (= 환각·일반론)

[AFTER — 사내 문서 RAG]
USER: "우리 회사 환불 기간은?"
검색: → "환불정책_2026.pdf" 검색
주입: → 해당 페이지 컨텍스트에 추가
AI:   "30일입니다. (출처: 환불정책_2026.pdf §2.1)"
```

## 라이브 시연 가능한 예시

### 시연 — Claude Code의 docs/ 자동 로드
```bash
[빈 프로젝트 — knowledge context 없음]
> "이 프로젝트의 PRD 알려줘"
AI:   "PRD를 찾을 수 없어 답변 불가"

[docs/PRD.md 추가 후]
> "이 프로젝트의 PRD 알려줘"
AI:   [docs/PRD.md 자동 로드]
      "비개발자 대상 바이브코딩 강의 자료..."
```

→ Claude Code 의 *자동 docs 로드* 자체가 knowledge context 의 가장 작은 사례.

## 4. 실제 사례 (2026 기준)

- **Notion AI Q&A**: 워크스페이스 전체 인덱싱. *"우리 팀 OKR이 뭐야?"* 답변.
- **Perplexity**: 매 질문 웹 검색 → 출처 표기. 2026년 MAU 1억 명.
- **Cursor `@` 명령**: 파일·심볼·웹·문서를 *명시적*으로 컨텍스트에 추가.
- **Claude Projects**: 사용자가 PDF·문서 업로드 후 — 모든 대화에서 자동 참조.
- **MCP `resources`** (자세히는 [MCP](../../tools/MCP.md)): 외부 시스템의 *읽기 전용 자료*를 표준 형식으로 주입.

## 한계 — GIGO

검색이 잘못되면 *근거 있는 환각*. 자세히는 [RAG.md 한계 섹션](../RAG.md#한계--gigo-실패-케이스).

```text
[실패 사례]
USER: "환불 정책"
검색: → 잘못된 *공급사 환불 가이드*가 1순위로 검색됨
AI:   "공급사로 직접 연락 후 7일..."  (= 정책이 *틀림*)
```

→ Knowledge context 도입 시 *검색 인덱싱 설계* 가 절반.

## 꼬리에 꼬리 (관련 개념)

- [컨텍스트 엔지니어링](../컨텍스트-엔지니어링.md) — 부모 문서
- [System Context](system-context.md), [Conversation Context](conversation-context.md), [Tool & Environment Context](tool-environment-context.md) — 다른 레이어들
- [RAG](../RAG.md) — Knowledge context 의 표준 구현
- [Knowledge Cutoff](../../phenomena/Knowledge-Cutoff.md) — Knowledge context 가 풀려는 핵심 문제
- [환각](../../phenomena/환각.md) — Knowledge context 의 핵심 적

## 출처

- [Anthropic — Use the right context (Engineering Blog)](https://www.anthropic.com/engineering/effective-context) — 공식 가이드
- [LangChain — RAG and context types](https://docs.langchain.com/oss/python/langchain/context-engineering) — RAG 통합 패턴
- [Pinecone — Retrieval-Augmented Generation](https://www.pinecone.io/learn/retrieval-augmented-generation/) — 벡터 검색 구현
