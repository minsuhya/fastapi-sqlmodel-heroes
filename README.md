# [maxmin93/fastapi-sqlmodel-heroes](https://github.com/maxmin93/fastapi-sqlmodel-heroes)

## About

Heroes tutorial with FastAPI, SqlModel, postgresql 14 and docker-compose

## 4. (FastAPI + SqlModel) Hero 튜토리얼 실행

SqlModel 의 Hero 튜토리얼을 FastAPI 프레임워크로 구현한 프로젝트

### 1) 실행화면 캡쳐

#### Backend: api

| ![](){: width="580"} |
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

| ![](){: width="580"} |
| :----: |
| &lt;그림&gt; Vue `/heroes` 화면 |


### 2) API 샘플

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

### 3) docker compose 실행

```bash
$ docker compose build


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
git remote add origin https://github.com/maxmin93/fastapi-sqlmodel-heroes.git
git push -u origin main

# 기존 리포지토리에 연결시
git remote add origin https://github.com/maxmin93/fastapi-sqlmodel-heroes.git
git branch -M main
git push -u origin main
```