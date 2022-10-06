# [maxmin93/fastapi-sqlmodel-heroes](https://github.com/maxmin93/fastapi-sqlmodel-heroes)

## About

Heroes tutorial with FastAPI, SqlModel, postgresql 14 and docker-compose

## 4. (FastAPI + SqlModel) Hero 튜토리얼 실행

SqlModel 의 Hero 튜토리얼을 FastAPI 프레임워크로 구현한 프로젝트

### 1) 실행화면 캡쳐

#### Backend: api

| <img alt="fastapi docs screen" src="https://github.com/maxmin93/fastapi-sqlmodel-heroes/blob/main/assets/img/06-fastapi-sqlmodel-pg14-docs-crunch.png?raw=true" style="width:580px;"/> |
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

| ![Vue heroes screen](/assets/img/12-fastapi-sqlmodel-pg14-docs-crunch.png){: width="580"} |
| :----: |
| &lt;그림&gt; Vue `/heroes` 화면 |


### 2) API 샘플

#### (1) create hero : POST `/heroes`

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

#### (2) update hero{id} : PATCH `/heroes/{id}`

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

#### (3) delete hero{id} : DELETE `/heroes/{id}`

```bash
# delete by ID=5
$ curl -X DELETE -H 'Accept: application/json' "http://localhost:58000/heroes/5"
{"ok":true}%


# select by ID=5 => 404 Error
$ curl -X GET -H 'Accept: application/json' "http://localhost:58000/hero/5"
{"detail":"Hero not found"}%
```

#### (4) select hero or heroes

- GET `/heroes/last`
- GET `/heroes`
- GET `/hero/2`

```bash
$ curl -X GET "http://localhost:58000/heroes/last"
{"name":"Spider-Boy","secret_name":"Pedro Parqueador","age":21,"team_id":null,"id":4}%
```

- select with relations : GET `/heroes/1`

```json
{
  "name": "Deadpond",
  "secret_name": "Dive Wilson",
  "age": null,
  "team_id": 1,
  "id": 1,
  "team": {
    "name": "서울팀",
    "headquarters": "종로구",
    "id": 1
  }
}
```

#### (5) create team : POST `/teams`

```bash
$ curl -X POST "http://localhost:8000/teams/" -H "Content-Type: application/json" -d '''
{"name": "뉴욕팀", "headquarters": "뉴욕시청", "heroes": []}
'''
{"name":"뉴욕팀","headquarters":"뉴욕시청","id":6}%

$ curl -X POST "http://localhost:8000/teams/" -H "Content-Type: application/json" -d '''
{"name": "뉴욕팀", "headquarters": "뉴욕시청", "heroes": [
  {"name":"Spider-Boy","secret_name":"Pedro Parqueador","age":21,"id":4}
]}
'''
{"name":"뉴욕팀","headquarters":"뉴욕시청","id":7}%
```

#### (6) update team{id} : PATCH `/teams/{id}`

```bash
# update partial-data by ID=5
$ curl -X PATCH "http://localhost:8000/teams/6" -H "Content-Type: application/json" -H 'Accept: application/json' -d '''
{"name": "뉴욕팀 Super", "headquarters": "뉴욕시청 공원", "heroes": [
  {"name":"Spider-Boy","secret_name":"Pedro Parqueador","age":21,"id":4}
]}
'''
{"name":"뉴욕팀 Super","headquarters":"뉴욕시청 공원","id":6}%
```

#### (3) delete team{id} : DELETE `/teams/{id}`

```bash
# delete by ID=5
$ curl -X DELETE -H 'Accept: application/json' "http://localhost:58000/teams/5"
{"ok":true}%


# select by ID=5 => 404 Error
$ curl -X GET -H 'Accept: application/json' "http://localhost:58000/teams/5"
{"detail":"Team not found"}%
```

#### (4) select team or teams

- GET `/teams/last`
- GET `/teams`
- GET `/team/2`

```bash
$ curl -X GET "http://localhost:58000/teams/last"
{"name":"Spider-Boy","secret_name":"Pedro Parqueador","age":21,"team_id":null,"id":4}%
```

- select with relations : GET `/teams/1`

```json
{
  "name": "서울팀",
  "headquarters": "종로구",
  "id": 1,
  "heroes": [
    {
      "name": "Deadpond",
      "secret_name": "Dive Wilson",
      "age": null,
      "team_id": 1,
      "id": 1
    },
    {
      "name": "Rusty-Man",
      "secret_name": "Tommy Sharp",
      "age": 48,
      "team_id": 1,
      "id": 2
    }
  ]
}
```

### 3) tutorials

#### (0) remove heroes and teams : GET `/tutorial/0`

- delete `select(Hero).where(Hero.name.match("%Tutorial%"))`
- delete `select(Team).where(Team.name.match("%Tutorial%"))`

#### (1) create heroes and teams : GET `/tutorial/1`

- create teams: ['Tutorial Preventers', 'Tutorial Z-Force']
- create heroes: ['Tutorial Deadpond', 'Tutorial Rusty-Man', 'Tutorial Spider-Boy']
  - 'Tutorial Deadpond'.team = 'Tutorial Z-Force'
  - 'Tutorial Rusty-Man'.team = 'Tutorial Preventers'

#### (2) select hero and team : GET `/tutorial/2`

- select hero `select(Hero).where(Hero.name == "Tutorial Spider-Boy")`
- select team `select(Team).where(Team.id == hero_spider_boy.team_id)`

#### (3) update hero with team : GET `/tutorial/3`

- update hero "Tutorial Spider-Boy"
  - hero_spider_boy.team = team_preventers  (팀 배정)
  
#### (4) delete team and update heroes : GET `/tutorial/4`

- delete team "Tutorial Preventers"
  + updated hero with none team

### 4) pytest

#### (1) `tests/main_test.py`

- test_hello : fastapi 작동 여부
- test_hero : GET `/heroes/last` 작동 여부와 HeroRead 변환
- test_aiohttp_with_every_client : 1000 번 GET `/heroes/` 호출
  + resp.status == 200 검사

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

#### (2) `tests/hero_test.py`

- test_read_items, test_read_item : select 테스트
- test_create_item : create 테스트
- test_update_item : update 테스트
- test_delete_item : delete 테스트

#### (3) `tests/team_test.py`

- test_read_groups, test_read_group : select 테스트
- test_create_group : create 테스트
- test_update_group : update 테스트
- test_delete_group: delete 테스트

  
### 4) docker compose 실행

```bash
# 도커 컴포즈에서 linux/amd64 이미지 생성 (Mac M1)
$ env DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose build
[+] Building 650.5s (20/21)
 => [internal] load build definition from Dockerfile                 0.0s
 => => transferring dockerfile: 32B                                  0.0s
 => [internal] load .dockerignore                                    0.0s
 => => transferring context: 34B                                     0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim   3.1s
...

$ docker compose up -d
[+] Running 2/2
 ⠿ Container smp-db   Created                                        0.0s
 ⠿ Container smp-api  Recreated                                      0.1s
Attaching to smp-api, smp-db
...

$ docker compose down -v
[+] Running 5/0
 ⠿ Container smp-api                Removed                          0.0s
 ⠿ Container smp-db                 Removed                          0.0s
 ⠿ Volume smpapi_data               Removed                          0.0s
 ⠿ Volume smpdb_data                Removed                          0.0s
 ⠿ Network sqlmodel-pg-api_default  Rem...                           0.1s
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