# Hero Tutorial of SqlModel

## 1. Storage: DB

API 서비스에 데이터를 제공하는 DB: postgresql 14

> 참고문서

- [hub.docker.com - postgres](https://hub.docker.com/_/postgres)

### 1) run image with postgres:14

```bash
# 바닐라 이미지 실행
$ docker run -it --rm --name pg14 -p 5432:5432/tcp \
  -e POSTGRES_DB=company_db \
  -e POSTGRES_USER=tonyne \
  -e POSTGRES_PASSWORD=tonyne \
  postgres:14

# DB 서비스만 실행 (포트 매핑이 안될 수 있음)
$ docker compose run -it --rm db

# 정상적인 포트 매핑 상태
$ docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                    NAMES
57e3284ccd7d   postgres:14   "docker-entrypoint.s…"   8 seconds ago   Up 7 seconds   0.0.0.0:5432->5432/tcp   jolly_lumiere
```


### 2) 시행착오 기록

#### ports 네트워크 매핑 확인

`0.0.0.0:5432->5432/tcp` 정보가 조회되어야 정상적으로 접근 가능

- `docker ps -a` 에서 이렇게 안뜨면 Host 와 포트 매핑이 안된것임
  + 이리저리 접속하려고 시도해봐야 헛수고!
    * network_mode 도 소용없고, md5 또는 trust 인증 변경도 소용없다
  + 포트 매핑이 안된 경우 '5432/tcp'만 출력된다

```bash
# 포트 매핑이 안된 경우 '5432/tcp'만 출력된다
$ docker ps -a
docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS      NAMES
5243a86275da   postgres:14   "docker-entrypoint.s…"   57 seconds ago   Up 55 seconds   5432/tcp   pg14
```

#### docker run 으로 정상실행 확인

postgresql 의 정상 작동은 docker run 으로 실행해 보는 것이 가장 정확하다.

- postgres 바닐라 이미지 실행 후, 
  + `docker ps -a` 로 포트 매핑 확인
  + `psql` 에 의한 USER/PASSWORD 정상접속을 확인할 것!

