# TOPIK 어휘 학습 및 퀴즈 웹 서비스
외국인 유학생을 위한 TOPIK(한국어능력시험) 어휘 학습 & 퀴즈 Flask 앱

## 실행 방법 (How to run)

```bash
pip install -r requirements.txt
python app.py
```ဗ

터미널에 나오는 주소로 접속하세요:
```
http://127.0.0.1:5000
```

## 폴더 구조 (Project structure)

```
topik_flask/
├── app.py            # Flask 라우트 (메인 서버 코드)
├── vocab.py           # 단어 데이터 (한국어/로마자/미얀마어/영어/예문)
├── requirements.txt   # 필요한 패키지 목록
├── templates/          # HTML 템플릿 (Jinja2)
│   ├── base.html
│   ├── index.html      # 홈 - 주제 선택
│   ├── study.html       # 학습 카드 (flashcard)
│   ├── quiz.html         # 퀴즈 문제
│   └── result.html       # 퀴즈 결과
└── static/
    └── style.css        # 디자인
```

## 기능 (Features)

- 주제(카테고리)별 단어 학습: 일상 / 학교 / 음식 / 여행 / 사회
- 학습 카드: 카드를 클릭하면 한국어 단어 → 미얀마어/영어 뜻 + 예문이 보여요
- 퀴즈: 4개 선택지 중 알맞은 뜻 고르기, 점수와 최고 기록 저장 (세션 기반)

## 단어 추가하는 방법 (How to add more words)

`vocab.py` 파일의 `VOCAB` 리스트에 아래 형식으로 딕셔너리를 추가하면 돼요:

```python
{"kr": "새 단어", "ro": "romanization", "my": "미얀마어 뜻",
 "en": "English meaning", "cat": "일상",
 "ex": "예문", "ex_my": "예문 미얀마어 번역"},
```

## 배포 (Deploying online)

팀 프로젝트 발표를 위해 온라인에 올리고 싶다면 **Render.com**이나
**PythonAnywhere**를 추천해요. GitHub에 이 폴더를 올린 뒤 연결하면 됩니다.
