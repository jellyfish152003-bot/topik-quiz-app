# -*- coding: utf-8 -*-
"""
TOPIK 어휘 학습 및 퀴즈 웹 서비스 (단일 파일 버전)
외국인 유학생을 위한 Flask 웹 애플리케이션 — ONE FILE ONLY

실행 방법 (How to run):
    pip install flask
    python app.py
    -> 브라우저에서 http://127.0.0.1:5000 접속

이 파일 하나만 있으면 됩니다. templates 폴더, static 폴더 필요 없어요.
This is the ONLY file you need. No templates/ or static/ folders required.
"""

import random
from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "topik-study-app-secret-key"  # 실제 배포 시에는 환경변수로 바꾸세요


# ============================================================
# 단어 데이터 (Vocabulary data)
# ============================================================
VOCAB = [
    {"kr": "안녕하다", "ro": "annyeonghada", "my": "နှုတ်ခွန်းဆက်သည်၊ ကျန်းမာသည်",
     "en": "to be well / hello", "cat": "일상",
     "ex": "오늘 기분이 안녕하세요?", "ex_my": "ဒီနေ့ စိတ်ခံစားချက် ကောင်းပါသလား?"},
    {"kr": "기숙사", "ro": "gisuksa", "my": "ကျောင်းအဆောင်",
     "en": "dormitory", "cat": "학교",
     "ex": "저는 기숙사에서 살아요.", "ex_my": "ကျွန်တော် ကျောင်းအဆောင်မှာ နေထိုင်ပါတယ်။"},
    {"kr": "등록금", "ro": "deungnokgeum", "my": "ကျောင်းလခ",
     "en": "tuition fee", "cat": "학교",
     "ex": "등록금이 많이 올랐어요.", "ex_my": "ကျောင်းလခ များစွာ တက်သွားတယ်။"},
    {"kr": "장학금", "ro": "janghakgeum", "my": "ပညာသင်ဆု",
     "en": "scholarship", "cat": "학교",
     "ex": "장학금을 받아서 기뻐요.", "ex_my": "ပညာသင်ဆု ရလို့ ဝမ်းသာပါတယ်။"},
    {"kr": "수강 신청", "ro": "sugang sincheong", "my": "ဘာသာရပ်စာရင်းသွင်းခြင်း",
     "en": "course registration", "cat": "학교",
     "ex": "수강 신청 기간이 언제예요?", "ex_my": "ဘာသာရပ်စာရင်းသွင်းချိန် ဘယ်တော့လဲ?"},
    {"kr": "과제", "ro": "gwaje", "my": "အိမ်စာ",
     "en": "assignment", "cat": "학교",
     "ex": "과제를 아직 못 끝냈어요.", "ex_my": "အိမ်စာကို မပြီးသေးဘူး။"},
    {"kr": "반찬", "ro": "banchan", "my": "ဟင်းလျာအထောက်အပံ့",
     "en": "side dish", "cat": "음식",
     "ex": "반찬이 정말 다양해요.", "ex_my": "ဟင်းလျာများ အလွန်စုံလင်ပါတယ်။"},
    {"kr": "배달", "ro": "baedal", "my": "အိမ်ပို့ဝန်ဆောင်မှု",
     "en": "delivery", "cat": "음식",
     "ex": "배달 앱으로 시켰어요.", "ex_my": "ပို့ဆောင်ရေး app နဲ့ မှာလိုက်တယ်။"},
    {"kr": "포장하다", "ro": "pojanghada", "my": "ထုပ်ပိုးသည်",
     "en": "to pack (takeout)", "cat": "음식",
     "ex": "남은 음식을 포장해 주세요.", "ex_my": "ကျန်တဲ့ အစားအစာကို ထုပ်ပေးပါ။"},
    {"kr": "편의점", "ro": "pyeonuijeom", "my": "အဆင်ပြေဆိုင်",
     "en": "convenience store", "cat": "일상",
     "ex": "편의점에서 김밥을 샀어요.", "ex_my": "အဆင်ပြေဆိုင်မှာ ကင်ဘတ် ဝယ်ခဲ့တယ်။"},
    {"kr": "환승", "ro": "hwanseung", "my": "ကားလွှဲစီးခြင်း",
     "en": "transfer (transit)", "cat": "여행",
     "ex": "여기서 지하철로 환승하세요.", "ex_my": "ဒီနေရာမှာ မြေအောက်ရထားကို ပြောင်းစီးပါ။"},
    {"kr": "왕복", "ro": "wangbok", "my": "အသွားအပြန်",
     "en": "round trip", "cat": "여행",
     "ex": "왕복 티켓이 더 싸요.", "ex_my": "အသွားအပြန်လက်မှတ် ပိုစျေးသက်ပါတယ်။"},
    {"kr": "숙소", "ro": "suksso", "my": "တည်းခိုစရာနေရာ",
     "en": "accommodation", "cat": "여행",
     "ex": "숙소를 아직 못 정했어요.", "ex_my": "တည်းခိုစရာနေရာကို မဆုံးဖြတ်ရသေးဘူး။"},
    {"kr": "관광지", "ro": "gwangwangji", "my": "ခရီးသွားစခန်း",
     "en": "tourist spot", "cat": "여행",
     "ex": "이 도시에는 관광지가 많아요.", "ex_my": "ဒီမြို့မှာ ခရီးသွားစခန်း အများကြီးရှိတယ်။"},
    {"kr": "비자", "ro": "bija", "my": "ဗီဇာ",
     "en": "visa", "cat": "사회",
     "ex": "비자를 연장해야 해요.", "ex_my": "ဗီဇာသက်တမ်း တိုးရမယ်။"},
    {"kr": "외국인등록증", "ro": "oegugin deungnokjeung", "my": "နိုင်ငံခြားသားမှတ်ပုံတင်ကတ်",
     "en": "alien registration card", "cat": "사회",
     "ex": "외국인등록증을 항상 가지고 다니세요.", "ex_my": "နိုင်ငံခြားသားကတ်ကို အမြဲယူဆောင်ပါ။"},
    {"kr": "취업", "ro": "chwieop", "my": "အလုပ်အကိုင်ရရှိခြင်း",
     "en": "employment", "cat": "사회",
     "ex": "졸업 후에 취업할 계획이에요.", "ex_my": "ဘွဲ့ရပြီးရင် အလုပ်ဝင်ဖို့ စီစဉ်ထားတယ်။"},
    {"kr": "경제", "ro": "gyeongje", "my": "စီးပွားရေး",
     "en": "economy", "cat": "사회",
     "ex": "요즘 경제 뉴스를 자주 봐요.", "ex_my": "ဒီနေ့ခေတ် စီးပွားရေးသတင်းကို မကြာခဏကြည့်ပါတယ်။"},
    {"kr": "환경", "ro": "hwangyeong", "my": "ပတ်ဝန်းကျင်",
     "en": "environment", "cat": "사회",
     "ex": "환경 보호가 중요해요.", "ex_my": "ပတ်ဝန်းကျင် ကာကွယ်ရေးက အရေးကြီးတယ်။"},
    {"kr": "습관", "ro": "seupgwan", "my": "အလေ့အကျင့်",
     "en": "habit", "cat": "일상",
     "ex": "좋은 습관을 만들고 싶어요.", "ex_my": "ကောင်းတဲ့အလေ့အကျင့် ဖြစ်စေချင်တယ်။"},
    {"kr": "성격", "ro": "seonggyeok", "my": "စရိုက်",
     "en": "personality", "cat": "일상",
     "ex": "제 성격은 활발해요.", "ex_my": "ကျွန်တော့်စရိုက်က တက်ကြွပါတယ်။"},
    {"kr": "고민", "ro": "gomin", "my": "စိတ်ပူပန်မှု",
     "en": "worry / concern", "cat": "일상",
     "ex": "요즘 고민이 많아요.", "ex_my": "ဒီနေ့ခေတ် စိတ်ပူစရာများနေတယ်။"},
    {"kr": "적응하다", "ro": "jeogeunghada", "my": "လိုက်လျောညီထွေဖြစ်သည်",
     "en": "to adapt", "cat": "일상",
     "ex": "새 환경에 적응 중이에요.", "ex_my": "ပတ်ဝန်းကျင်အသစ်နဲ့ လိုက်လျောညီထွေဖြစ်နေတယ်။"},
    {"kr": "발표", "ro": "balpyo", "my": "တင်ပြချက်",
     "en": "presentation", "cat": "학교",
     "ex": "내일 발표가 있어요.", "ex_my": "မနက်ဖြန် တင်ပြချက်ရှိတယ်။"},
    {"kr": "동아리", "ro": "dongari", "my": "ကလပ်",
     "en": "club (school)", "cat": "학교",
     "ex": "동아리 활동이 재미있어요.", "ex_my": "ကလပ်လှုပ်ရှားမှု စိတ်ဝင်စားစရာကောင်းတယ်။"},
]

CATEGORIES = ["전체", "일상", "학교", "음식", "여행", "사회"]


def get_by_category(cat):
    if cat == "전체" or not cat:
        return list(VOCAB)
    return [w for w in VOCAB if w["cat"] == cat]


# ============================================================
# 공통 스타일 + 레이아웃 (CSS embedded directly, no static folder)
# ============================================================
BASE_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans+Myanmar:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#FAF6EC; --ink:#22201B; --ink-soft:#5B564C;
    --jade:#2F6F62; --jade-deep:#1F4F45; --clay:#B5502F;
    --line:#DED4BC; --card:#FFFFFF; --radius:4px;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{background:var(--paper);color:var(--ink);
    font-family:'Noto Sans KR','Noto Sans Myanmar',sans-serif;min-height:100vh;}
  .my{font-family:'Noto Sans Myanmar','Noto Sans KR',sans-serif;}
  a{text-decoration:none;color:inherit;}
  .wrap{max-width:760px;margin:0 auto;padding:28px 20px 80px;}
  header.top{display:flex;align-items:flex-start;justify-content:space-between;
    gap:16px;border-bottom:1px solid var(--line);padding-bottom:18px;margin-bottom:24px;}
  .brand h1{font-family:'Noto Serif KR',serif;font-weight:700;font-size:1.7rem;margin:0 0 4px;}
  .brand .sub{font-size:0.92rem;color:var(--ink-soft);margin:0;}
  .mark{width:44px;height:44px;flex:none;border-radius:50%;
    background:radial-gradient(circle at 34% 34%, var(--jade) 0 34%, transparent 35%),
                radial-gradient(circle at 66% 66%, var(--clay) 0 34%, transparent 35%);
    background-color:var(--card);border:1px solid var(--line);}
  .lead{font-size:0.98rem;margin:0 0 4px;}
  .lead.my{color:var(--ink-soft);margin-bottom:22px;}
  .cat-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
  @media (max-width:480px){.cat-grid{grid-template-columns:1fr;}}
  .cat-card{border:1px solid var(--line);background:var(--card);border-radius:var(--radius);padding:18px;}
  .cat-card h3{font-family:'Noto Serif KR',serif;margin:0 0 12px;font-size:1.15rem;}
  .cat-actions{display:flex;gap:8px;flex-wrap:wrap;}
  .chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px;}
  .chip{border:1px solid var(--line);background:var(--card);color:var(--ink-soft);
    font-size:0.85rem;padding:6px 13px;border-radius:999px;}
  .chip.active{background:var(--jade-deep);border-color:var(--jade-deep);color:var(--paper);}
  .btn{display:inline-block;font-size:0.92rem;font-weight:500;padding:10px 18px;
    border-radius:var(--radius);border:1px solid var(--line);background:var(--card);
    color:var(--ink);cursor:pointer;}
  .btn.primary{background:var(--jade-deep);border-color:var(--jade-deep);color:var(--paper);}
  .btn.ghost{background:transparent;}
  .row-actions{display:flex;gap:10px;justify-content:center;margin-top:20px;flex-wrap:wrap;}
  .deck{display:flex;flex-direction:column;gap:16px;margin-bottom:10px;}
  .flip-card{perspective:1400px;height:230px;cursor:pointer;}
  .flip-inner{position:relative;width:100%;height:100%;transform-style:preserve-3d;
    transition:transform .5s cubic-bezier(.4,.2,.2,1);}
  .flip-card.flipped .flip-inner{transform:rotateY(180deg);}
  .face{position:absolute;inset:0;backface-visibility:hidden;background:var(--card);
    border:1px solid var(--line);border-radius:var(--radius);display:flex;flex-direction:column;
    align-items:center;justify-content:center;text-align:center;padding:24px;}
  .face.back{transform:rotateY(180deg);}
  .cat-tag{font-size:0.72rem;color:var(--jade-deep);border:1px solid var(--jade-deep);
    border-radius:999px;padding:2px 10px;margin-bottom:14px;}
  .kr-word{font-family:'Noto Serif KR',serif;font-weight:700;font-size:2rem;margin:0 0 8px;}
  .roman{color:var(--ink-soft);font-size:0.95rem;margin:0 0 16px;}
  .hint{font-size:0.8rem;color:var(--ink-soft);}
  .my-meaning{font-size:1.3rem;font-weight:500;margin:0 0 6px;}
  .en-meaning{color:var(--ink-soft);font-size:0.9rem;margin:0 0 14px;}
  .example{border-top:1px solid var(--line);padding-top:12px;width:100%;}
  .example .kr-ex{font-size:0.95rem;margin:0 0 4px;}
  .example .my-ex{font-size:0.88rem;color:var(--ink-soft);margin:0;}
  .quiz-head{display:flex;justify-content:space-between;align-items:baseline;
    margin-bottom:16px;font-size:0.88rem;color:var(--ink-soft);}
  .quiz-head strong{color:var(--ink);font-family:'Noto Serif KR',serif;}
  .qcard{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
    padding:34px 26px;text-align:center;margin-bottom:18px;}
  .qcard .kr-word{font-size:2.1rem;margin-bottom:6px;}
  .qprompt{margin:0 0 16px;font-size:0.85rem;color:var(--ink-soft);text-align:center;}
  .choices{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
  @media (max-width:480px){.choices{grid-template-columns:1fr;}}
  .choice{font-family:'Noto Sans Myanmar','Noto Sans KR',sans-serif;text-align:left;
    padding:14px 16px;border:1px solid var(--line);background:var(--card);
    border-radius:var(--radius);cursor:pointer;font-size:0.98rem;color:var(--ink);width:100%;}
  .choice:hover{border-color:var(--jade);}
  .result .score{font-family:'Noto Serif KR',serif;font-size:3rem;font-weight:700;margin:8px 0;}
  .result .best{color:var(--ink-soft);font-size:0.9rem;margin-bottom:6px;}
  footer.note{margin-top:30px;font-size:0.78rem;color:var(--ink-soft);text-align:center;}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <a href="{{ url_for('home') }}">
      <div class="brand">
        <h1>TOPIK 어휘</h1>
        <p class="sub">외국인 유학생을 위한 어휘 학습 및 퀴즈</p>
        <p class="sub my">TOPIK ဝေါဟာရ လေ့လာမှုနှင့် စာမေးပွဲ</p>
      </div>
    </a>
    <div class="mark"></div>
  </header>

  {{ body|safe }}

  <footer class="note">Flask 단일 파일 버전 · Flask တစ်ဖိုင်တည်း ဗားရှင်း</footer>
</div>
</body>
</html>
"""

INDEX_BODY = """
<p class="lead">주제를 선택하고 학습 방식을 골라보세요.</p>
<p class="lead my">အကြောင်းအရာကို ရွေးပြီး လေ့လာရမည့်ပုံစံကို ရွေးပါ။</p>
<div class="cat-grid">
  {% for cat in categories %}
  <div class="cat-card">
    <h3>{{ cat }}</h3>
    <div class="cat-actions">
      <a class="btn" href="{{ url_for('study', cat=cat) }}">학습 카드</a>
      <a class="btn primary" href="{{ url_for('quiz_start', cat=cat) }}">퀴즈 시작</a>
    </div>
  </div>
  {% endfor %}
</div>
"""

STUDY_BODY = """
<div class="chips">
  {% for cat in categories %}
    <a class="chip {% if cat == current_cat %}active{% endif %}"
       href="{{ url_for('study', cat=cat) }}">{{ cat }}</a>
  {% endfor %}
</div>
{% if words %}
<div class="deck">
  {% for w in words %}
  <div class="flip-card" onclick="this.classList.toggle('flipped')">
    <div class="flip-inner">
      <div class="face front">
        <span class="cat-tag">{{ w.cat }}</span>
        <p class="kr-word">{{ w.kr }}</p>
        <p class="roman">[{{ w.ro }}]</p>
        <p class="hint">눌러서 뜻 보기 · အဓိပ္ပာယ်ကြည့်ရန် နှိပ်ပါ</p>
      </div>
      <div class="face back">
        <p class="my-meaning my">{{ w.my }}</p>
        <p class="en-meaning">{{ w.en }}</p>
        <div class="example">
          <p class="kr-ex">{{ w.ex }}</p>
          <p class="my-ex my">{{ w.ex_my }}</p>
        </div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>
{% else %}
<p class="lead">이 주제에는 아직 단어가 없어요.</p>
{% endif %}
<div class="row-actions">
  <a class="btn primary" href="{{ url_for('quiz_start', cat=current_cat) }}">이 주제로 퀴즈 풀기</a>
  <a class="btn ghost" href="{{ url_for('home') }}">홈으로</a>
</div>
"""

QUIZ_BODY = """
<div class="quiz-head">
  <span>문제 {{ q_num }} / {{ q_total }}</span>
  <strong>점수 {{ score }}</strong>
</div>
<div class="qcard">
  <p class="kr-word">{{ word.kr }}</p>
  <p class="roman">[{{ word.ro }}]</p>
</div>
<p class="qprompt">알맞은 뜻을 고르세요 · မှန်ကန်သောအဓိပ္ပာယ်ကို ရွေးပါ</p>
<form method="post" action="{{ url_for('quiz_answer') }}">
  <div class="choices">
    {% for opt in options %}
    <button type="submit" name="choice" value="{{ opt }}" class="choice">{{ opt }}</button>
    {% endfor %}
  </div>
</form>
"""

RESULT_BODY = """
<div class="qcard result">
  <p class="hint">퀴즈 완료 · စာမေးပွဲ ပြီးဆုံးပါပြီ</p>
  <p class="score">{{ score }} / {{ total }}</p>
  <p class="best">최고 기록 : {{ best }} / {{ total }}</p>
  <div class="row-actions">
    <a class="btn primary" href="{{ url_for('quiz_start', cat=cat) }}">다시 풀기</a>
    <a class="btn ghost" href="{{ url_for('home') }}">홈으로</a>
  </div>
</div>
"""


def page(title, body_template, **ctx):
    """본문 템플릿을 렌더링한 뒤 기본 레이아웃 안에 끼워 넣어요."""
    body_html = render_template_string(body_template, **ctx)
    return render_template_string(BASE_HTML, title=title, body=body_html)


# ============================================================
# 라우트 (Routes)
# ============================================================
@app.route("/")
def home():
    return page("TOPIK 어휘 — 홈", INDEX_BODY, categories=CATEGORIES)


@app.route("/study")
def study():
    cat = request.args.get("cat", "전체")
    words = get_by_category(cat)
    return page("학습 카드 — " + cat, STUDY_BODY,
                categories=CATEGORIES, current_cat=cat, words=words)


@app.route("/quiz/start")
def quiz_start():
    cat = request.args.get("cat", "전체")
    pool = get_by_category(cat)
    random.shuffle(pool)
    pool = pool[:8] if len(pool) > 8 else pool

    session["quiz_cat"] = cat
    session["quiz_words"] = pool
    session["quiz_idx"] = 0
    session["quiz_score"] = 0
    return redirect(url_for("quiz"))


@app.route("/quiz")
def quiz():
    words = session.get("quiz_words")
    if not words or len(words) < 4:
        return redirect(url_for("home"))

    idx = session.get("quiz_idx", 0)
    if idx >= len(words):
        return redirect(url_for("quiz_result"))

    current = words[idx]
    wrong_pool = [w for w in VOCAB if w["kr"] != current["kr"]]
    wrongs = random.sample(wrong_pool, 3)
    options = [current["my"]] + [w["my"] for w in wrongs]
    random.shuffle(options)

    return page("퀴즈 — 문제 " + str(idx + 1), QUIZ_BODY,
                word=current, options=options,
                q_num=idx + 1, q_total=len(words),
                score=session.get("quiz_score", 0))


@app.route("/quiz/answer", methods=["POST"])
def quiz_answer():
    words = session.get("quiz_words")
    idx = session.get("quiz_idx", 0)
    if not words or idx >= len(words):
        return redirect(url_for("home"))

    selected = request.form.get("choice")
    if selected == words[idx]["my"]:
        session["quiz_score"] = session.get("quiz_score", 0) + 1

    session["quiz_idx"] = idx + 1
    return redirect(url_for("quiz"))


@app.route("/quiz/result")
def quiz_result():
    words = session.get("quiz_words", [])
    score = session.get("quiz_score", 0)
    total = len(words)

    best = session.get("best_score", 0)
    if score > best:
        best = score
        session["best_score"] = best

    return page("퀴즈 결과", RESULT_BODY,
                score=score, total=total, best=best,
                cat=session.get("quiz_cat", "전체"))


if __name__ == "__main__":
    app.run(debug=True)
