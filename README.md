# [maxmin93/fastapi-sqlmodel-heroes](https://github.com/maxmin93/fastapi-sqlmodel-heroes)

## About

Heroes tutorial with FastAPI, SqlModel, postgresql 14 and docker-compose

## 4. (FastAPI + SqlModel) Hero 튜토리얼 실행

SqlModel 의 Hero 튜토리얼을 FastAPI 프레임워크로 구현한 프로젝트

### 1) 실행화면 캡쳐

#### Backend: api

| <img alt="fastapi docs screen" src="https://github.com/maxmin93/fastapi-sqlmodel-heroes/blob/main/assets/img/12-fastapi-sqlmodel-pg14-docs-crunch.png?raw=true" style="width:580px;"/> |
| :----: |
| &lt;그림&gt; FastAPI `/docs` 화면 |

#### Storage: db

```sql
$ psql -d company_db -U tonyne -h localhost -p 5432 -W
Password:
psql (14.5)
Type "help" for help.

company_db=# select * from hero;
    name    |   secret_name    | age | id
------------+------------------+-----+----
 Deadpond   | Dive Wilson      |     |  1
 Rusty-Man  | Tommy Sharp      |  48 |  2
 Dormammu   | Unknown          |     |  3
 Spider-Boy | Pedro Parqueador |  21 |  4
(4 rows)
```

#### Frontend: web

| ![Vue heroes screen](/assets/img/12-fastapi-sqlmodel-pg14-docs-crunch/png){: width="580"} |
| :----: |
| &lt;그림&gt; Vue `/heroes` 화면 |


### 2) API 샘플

#### POST `/heroes`

```bash
# insert with HeroCreate
$ curl -X POST "http://localhost:58000/heroes/" -H "Content-Type: application/json" -d '''
{"name": "ABC Teacher", "secret_name": "foo bar", "age": 35}
'''
{"name":"ABC Teacher","secret_name":"foo bar","age":35,"id":5}%


# select by ID=5
$ curl -X GET "http://localhost:58000/hero/5"
{"name":"ABC Teacher","secret_name":"foo bar","age":35,"id":5}%
```

#### PATCH `/heroes/{id}`

```bash
# update whole-data by ID=5
$ curl -X PATCH "http://localhost:58000/heroes/5" -H "Content-Type: application/json" -H 'Accept: application/json' -d '''
{"name": "ABC Teacher (Extra)", "secret_name": "foo bar", "age": 55}
'''
{"name":"ABC Teacher","secret_name":"foo bar","age":35,"id":5}%


# update partial-data by ID=5
$ curl -X PATCH "http://localhost:58000/heroes/5" -H "Content-Type: application/json" -H 'Accept: application/json' -d '''
{"name": "ABC Super Teacher (Extra)"}
'''
{"name":"ABC Super Teacher (Extra)","secret_name":"foo bar","age":55,"id":5}%


# select by ID=5
$ curl -X GET -H 'Accept: application/json' "http://localhost:58000/hero/5"
{"name":"ABC Teacher Teacher (Extra)","secret_name":"foo bar","age":55,"id":5}%
```

#### DELETE `/heroes/{id}`

```bash
# delete by ID=5
$ curl -X DELETE -H 'Accept: application/json' "http://localhost:58000/heroes/5"
{"ok":true}%


# select by ID=5 => 404 Error
$ curl -X GET -H 'Accept: application/json' "http://localhost:58000/hero/5"
{"detail":"Hero not found"}%
```

#### GET `/heroes`

```json
[
  {
    "name": "Deadpond",
    "secret_name": "Dive Wilson",
    "age": null,
    "id": 1
  },{
    "name": "Rusty-Man",
    "secret_name": "Tommy Sharp",
    "age": 48,
    "id": 2
  },{
    "name": "Dormammu",
    "secret_name": "Unknown",
    "age": null,
    "id": 3
  },{
    "name": "Spider-Boy",
    "secret_name": "Pedro Parqueador",
    "age": 21,
    "id": 4
  }
]
```

#### GET `/hero/2`

```json
{
  "name": "Rusty-Man",
  "secret_name": "Tommy Sharp",
  "age": 48,
  "id": 2
}
```

### 3) pytest

`tests/main_test.py` 에 작성

```bash
$ poetry run pytest tests --log-cli-level=DEBUG
============================== test session starts ===============================
platform darwin -- Python 3.9.13, pytest-7.1.3, pluggy-1.0.0
rootdir: /Users/bgmin/Workspaces/python/sqlmodel/sqlmodel-pg-api/smp-api
plugins: anyio-3.6.1
collected 6 items

tests/main_test.py::test_hello
tests/main_test.py::test_read_items
tests/main_test.py::test_read_item
tests/main_test.py::test_create_item
tests/main_test.py::test_update_item
tests/main_test.py::test_delete_item

tests/main_test.py ......                                                  [100%]

=============================== 6 passed in 0.64s ================================
```


### 4) docker compose 실행

```bash
# 도커 컴포즈에서 linux/amd64 이미지 생성
$ env DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose build


$ docker compose run --rm db


$ docker compose up -d


$ docker compose down -v
```

> 참고

```
# 신규 리포지토리에 연결시
git init
git add --all
git commit -m "first commit"
git branch -M main
git remote add origin $GITHUB/maxmin93/fastapi-sqlmodel-heroes.git
git push -u origin main

# 기존 리포지토리에 연결시
git remote add origin https://github.com/maxmin93/fastapi-sqlmodel-heroes.git
git branch -M main
git push -u origin main
```