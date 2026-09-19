# -*- coding: utf-8 -*-
"""
TOPIK 어휘 학습 및 퀴즈 웹 서비스
외국인 유학생을 위한 Flask 웹 애플리케이션

실행 방법 (How to run):
    pip install -r requirements.txt
    python app.py
    -> 브라우저에서 http://127.0.0.1:5000 접속
"""

import random
from flask import Flask, render_template, request, session, redirect, url_for

from vocab import VOCAB, CATEGORIES, get_by_category

app = Flask(__name__)
app.secret_key = "topik-study-app-secret-key"  # 실제 배포 시에는 환경변수로 바꾸세요


# ---------------------------------------------------------
# 홈 화면 : 카테고리 선택
# ---------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html", categories=CATEGORIES)


# ---------------------------------------------------------
# 학습 카드 (Flashcard) 화면
# ---------------------------------------------------------
@app.route("/study")
def study():
    cat = request.args.get("cat", "전체")
    words = get_by_category(cat)
    return render_template(
        "study.html",
        categories=CATEGORIES,
        current_cat=cat,
        words=words,
    )


# ---------------------------------------------------------
# 퀴즈 시작 : 세션에 퀴즈 상태를 만들어요
# ---------------------------------------------------------
@app.route("/quiz/start")
def quiz_start():
    cat = request.args.get("cat", "전체")
    pool = get_by_category(cat)
    random.shuffle(pool)
    pool = pool[:8] if len(pool) > 8 else pool

    session["quiz_cat"] = cat
    session["quiz_words"] = pool          # 이번 퀴즈에 나올 단어들
    session["quiz_idx"] = 0
    session["quiz_score"] = 0

    return redirect(url_for("quiz"))


# ---------------------------------------------------------
# 퀴즈 문제 화면
# ---------------------------------------------------------
@app.route("/quiz")
def quiz():
    words = session.get("quiz_words")
    if not words or len(words) < 4:
        return redirect(url_for("home"))

    idx = session.get("quiz_idx", 0)

    if idx >= len(words):
        return redirect(url_for("quiz_result"))

    current = words[idx]

    # 오답 선택지 3개를 전체 단어에서 무작위로 뽑아요
    wrong_pool = [w for w in VOCAB if w["kr"] != current["kr"]]
    wrongs = random.sample(wrong_pool, 3)
    options = [current["my"]] + [w["my"] for w in wrongs]
    random.shuffle(options)

    return render_template(
        "quiz.html",
        word=current,
        options=options,
        q_num=idx + 1,
        q_total=len(words),
        score=session.get("quiz_score", 0),
    )


# ---------------------------------------------------------
# 퀴즈 정답 제출
# ---------------------------------------------------------
@app.route("/quiz/answer", methods=["POST"])
def quiz_answer():
    words = session.get("quiz_words")
    idx = session.get("quiz_idx", 0)
    if not words or idx >= len(words):
        return redirect(url_for("home"))

    selected = request.form.get("choice")
    correct_meaning = words[idx]["my"]

    if selected == correct_meaning:
        session["quiz_score"] = session.get("quiz_score", 0) + 1

    session["quiz_idx"] = idx + 1
    return redirect(url_for("quiz"))


# ---------------------------------------------------------
# 퀴즈 결과 화면
# ---------------------------------------------------------
@app.route("/quiz/result")
def quiz_result():
    words = session.get("quiz_words", [])
    score = session.get("quiz_score", 0)
    total = len(words)

    best = session.get("best_score", 0)
    if score > best:
        best = score
        session["best_score"] = best

    return render_template(
        "result.html",
        score=score,
        total=total,
        best=best,
        cat=session.get("quiz_cat", "전체"),
    )


if __name__ == "__main__":
    app.run(debug=True)
