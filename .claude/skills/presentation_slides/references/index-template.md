# Index.html 전체 템플릿

index.html은 네비게이션 바 없이 허브 페이지로 동작. `navigateTo()` 함수는 카드 링크용으로 포함.
섹션 그룹화/색상 코딩 없이 **단일 4열 그리드**로 모든 슬라이드를 균일하게 나열한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>{{프레젠테이션 제목}} — 비주얼 자료</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0a0f1a;
  font-family: 'Noto Sans KR', sans-serif;
  color: #e6edf3;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  padding: 60px 0 80px;
}
.container { width: 1280px; padding: 0 80px; }
.page-title {
  font-size: 42px; font-weight: 900;
  background: linear-gradient(135deg, #7c3aed, #38bdf8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  text-align: center; margin-bottom: 10px;
}
.page-subtitle {
  text-align: center; font-size: 16px; color: #8b949e; margin-bottom: 50px;
}

/* Grid (단일, 섹션 그룹 없음) */
.grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
}
.card {
  display: flex; flex-direction: column; gap: 6px; padding: 18px 20px;
  background: rgba(139,148,158,0.04);
  border: 1px solid rgba(139,148,158,0.1);
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.25s ease;
}
.card:hover {
  transform: translateY(-3px);
  border-color: rgba(139,148,158,0.25);
  box-shadow: 0 8px 32px rgba(139, 148, 158, 0.12);
}
.card .card-num {
  font-size: 28px; font-weight: 900; color: #c9d1d9;
}
.card .card-title {
  font-size: 14px; font-weight: 700; color: #c9d1d9;
}
.card .card-file {
  font-size: 11px; color: #484f58; font-family: 'Courier New', monospace;
}

/* 페이지 전환 애니메이션 */
body { opacity: 0; animation: fadeIn 0.4s ease forwards; }
body.fade-out { animation: fadeOut 0.3s ease forwards; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-12px); }
}
</style>
</head>
<body>
<div class="container">
  <h1 class="page-title">{{프레젠테이션 제목}} — 비주얼 자료</h1>
  <p class="page-subtitle">전체 {{TOTAL}}개 슬라이드 · 클릭하여 개별 페이지로 이동</p>

  <div class="grid">
    <a class="card" href="{{파일명}}" onclick="event.preventDefault(); navigateTo(this.href)">
      <span class="card-num">{{NN}}</span>
      <span class="card-title">{{슬라이드 제목}}</span>
      <span class="card-file">{{파일명}}</span>
    </a>
    <!-- 카드 반복 (모든 슬라이드를 단일 그리드에 균일하게) -->
  </div>
</div>

<script>
function navigateTo(url) {
  document.body.classList.add('fade-out');
  setTimeout(function() { window.location.href = url; }, 300);
}
</script>
</body>
</html>
```

**핵심 규칙:**
- index.html에는 nav 바 없음
- `navigateTo()`는 카드 클릭 전환용
- **단일 4열 그리드** — 섹션 그룹/헤더/색상 코딩 없음
- 모든 카드 동일한 스타일 (호버 시 보더만 살짝 밝아짐)
