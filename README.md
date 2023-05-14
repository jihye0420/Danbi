# **Danbi -TaskAPI**

🔥 **단비교육 사전과제**

## **프로젝트 시작 방법**

### Install

- [python 3.9.6](https://www.python.org/downloads/release/python-396/)
- mysql

### **Requirements** & **Project Setup**

- 외부 라이브러리(simple-jwt 등)을 사용했으므로 requirements.txt에 작성된 꼭 다운로드 해주셔야 합니다.
- 테스트용 DB 및 SECRET_KEY 사용을 위해 `python manage.py` command 사용시 `-settings=config.settings.local` 옵션을 사용
- 로컬에서 실행할 경우

```bash
# 파이썬 설치 필수
 
# 프로젝트 clone (로컬로 내려받기)
$ git clone https://github.com/jihye0420/Danbi.git
$ cd ${디렉터리 명} (ex) cd Danbi)

# 가상환경 생성
$ python -m venv ${가상환경명} (ex) python -m venv venv)

# 가상환경 활성화
$ source ${가상환경명}/bin/activate  # 맥
$ source ${가상환경명}/Scripts/activate  # 윈도우

# Then install the dependencies
(venv)$ pip install -r requirements.txt

# Django settings (DB 생성)
(venv)$ python manage.py makemigrations --settings=config.settings.local
(venv)$ python manage.py migrate --settings=config.settings.local

# 실행
(venv)$ python manage.py runserver --settings=config.settings.local
```

- .env 파일
    - [django secret key 생성 사이트](https://djecrety.ir/)
        
        ![https://user-images.githubusercontent.com/95459089/236672311-f2839045-0ecd-4175-8e6a-f723e85fbf65.png](https://user-images.githubusercontent.com/95459089/236672311-f2839045-0ecd-4175-8e6a-f723e85fbf65.png)
        
    - 이동 후, Generate 클릭 후 키 복사 후 `config >> settings` 폴더 하위에 .env 파일 생성 하기
    - **위의 사이트에서 생성한 secret key를 SECRET_KEY= 넣어주기**
    - **나머지는 위의 그림처럼 입력**
    
    ```bash
    SECRET_KEY=
    DEBUG=True
    DATABASE_NAME=danbi
    DATABASE_USER=사용자 (ex) root)
    DATABASE_PASSWORD=사용자 비밀번호 (ex) 1234)
    DATABASE_HOST=localhost
    DATABASE_PORT=3306
    ```
    

## 📝 **프로젝트 개요**

Django Rest Framework 

- 유저 회원가입, 로그인(JWT 토큰 인증 방식) 기능
- Task 생성, 수정, 조회 기능

### **개발 기간**

- 2023.05.13 - 2022.05.14 (2일)

### 기능 목록

| 버전 | 기능 | API | 세부 기능 | 설명 | 상태 |
| --- | --- | --- | --- | --- | --- |
| v1 | Users | POST /users/signup | 회원가입 | 회원가입 | ✅ |
| - | - | POST /users/login | 로그인 | jwt를 이용한 로그인 | ✅ |
| - | - | POST /users/token/refresh | 토큰 재발급 | 토큰 재발급 | ✅ |
| - | Task | GET /task | 상위 + 하위 업무 조회 | 상위 + 하위 업무 조회 | ✅ |
| - | - | GET /task/:id | 상위 + 하위 업무 상세 조회 | 상위 + 하위 업무 상세 조회 | ✅ |
| - | - | POST /task | 상위 업무 등록 | Task 등록 | ✅ |
| - | - | PUT /task/:id | 상위 업무 수정  | Task 수정 (제목, 내용, 팀, 완료 처리) | ✅ |
| - | - | PUT /task/sub/:subId | 하위 업무 수정 | SubTask 수정 (완료 처리) | ✅ |
| - | 테스트 | - | 테스트 | 기능, 전체 테스트 | - |

🔥 추가 기능 구현시 업데이트 예정

## ⚒️ **프로젝트 기술 스택**


### **Backend**

### **DB**

### **Tools**

## ㏈ ERD

![image](https://github.com/jihye0420/Danbi/assets/50284754/eb6442d7-4087-4e57-bcdb-7c3a06f22643)

- USER ↔ Task (1:N)
- User model
    - User 모델은 Django의 `AbstractBaseUser`를 overriding
    - Team ↔ User  (1:N)
    - User ↔ Task (1:N)
- Task model
    - Task ↔ SubTask (1:N)

## API 명세


[POSTMAN API DOCS](https://documenter.getpostman.com/view/19274775/2s847LMBGN)

## 🌳 프로젝트 구조


```bash
.
├── README.md
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings
│   │   ├── base.py
│   │   ├── local.py
│   │   └── permissions.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── task
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── users
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── utils
│   └── response.py
└── venv
    ├── bin
    ├── lib
    ├── pyvenv.cfg
    └── share
```
