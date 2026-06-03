# Trash Diary API

AI와 채팅으로 감정을 털어놓고, 대화를 버리는 감정 일기 서비스의 FastAPI 백엔드

---

## 기술 스택

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Auth**: JWT (Access Token + Refresh Token)
- **Password**: bcrypt

---

## 프로젝트 구조

```
app/
├── core/
│   ├── config.py         # 환경변수 로드
│   └── security.py       # JWT 생성/검증, 비밀번호 해싱
├── routers/
│   └── auth.py           # Auth API
├── schemas/
│   ├── auth.py           # 요청/응답 스키마
│   └── user.py           # 유저 스키마
├── database.py           # PostgreSQL 연결 풀
├── dependencies.py       # JWT 인증 미들웨어
├── redis_client.py       # Refresh Token 관리
└── main.py               # 앱 진입점
```

---

## 시작하기

### 1. 가상환경 설치

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일 생성 후 아래 내용 입력

```env
DATABASE_URL=postgresql://postgres:비밀번호@localhost:5432/trash_bin_diary_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. 서버 실행

```bash
uvicorn app.main:app --reload
```

### 4. API 문서 확인

```
http://localhost:8000/docs
```

---

## API 목록

| Method | Path | 설명 | 인증 |
|---|---|---|---|
| POST | /auth/register | 회원가입 | 없음 |
| POST | /auth/login | 로그인 | 없음 |
| POST | /auth/refresh | 토큰 재발급 | 없음 |
| POST | /auth/logout | 로그아웃 | 없음 |

---

## 환경

- Python 3.13
- PostgreSQL 15+
- Redis 7+
