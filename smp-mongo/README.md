# Hero Tutorial of SqlModel

## 2. Storage: MongoDB

API 서비스에 업로드 파일을 넣고 데이터를 제공하는 DB: `mongo:6`

> 참고문서

- [hub.docker.com - mongo](https://hub.docker.com/_/mongo)

### 1) run image with mongo:6

```bash
# 바닐라 이미지 실행
$ docker run -it --rm --name mgdb -p 27017:27017/tcp \
  -e MONGO_INITDB_ROOT_USERNAME=tonyne \
  -e MONGO_INITDB_ROOT_PASSWORD=tonyne \
  mongo:6

# DB 서비스만 실행 (포트 매핑이 안될 수 있음)
$ docker compose run -it --rm mongo

# 정상적인 포트 매핑 상태
$ docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                    NAMES
d28c5262685f   mongo:6       "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes   0.0.0.0:27017->27017/tcp   smp-mongo
```


### 2) 시행착오 기록

#### (1) volume 생성 : data and configdb

볼륨이 두개 필요하다. (설정 안해도 랜덤 이름으로 2개 생성됨)

#### (2) 'ObjectId' object is not iterable

```
ValueError: [TypeError("'ObjectId' object is not iterable"), TypeError('vars() argument must have __dict__ attribute')]
```

csv 파일을 업로드 할 때, FastAPI 에서 ObjectId `_id` 값의 JSON 타입 변환 과정에 오류가 발생

- FastAPI 사용시에만 발생하는 문제
- Pydantic 의 BaseModel 클래스 생성시 ObjectId 처리하는 config 필요
  + 간단한 방법으로, `_id` 값을 강제로 문자열로 변환하여 사용

> csv 파일 임포트와 mongoDB 입력 (insert_many)

```python
@router.post("/upload")
def reader_upload(file: UploadFile = File(...), *, db: Database = Depends(get_mongodb)):
    """
    curl -F 'file=@../assets/data/test.csv' -X POST "http://localhost:8000/files/upload"
    """
    csvReader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"))
    rows = []
    for row in csvReader:
        row["_id"] = str(row.pop("id"))
        rows.append(row)
    file.file.close()

    collection_name = os.path.splitext(file.filename)[0]
    inserted_ids = insert_data(db[collection_name], rows)
    logger.info(f"coll['{collection_name}'].ids = {inserted_ids}")
    return rows
```

FastAPI, MongoDB, ObjectID 관련 참고자료

- [Handling MongoDB ObjectId in Python-fastAPI](https://medium.com/@madhuri.pednekar/handling-mongodb-objectid-in-python-fastapi-4dd1c7ad67cd)
  + JSONEncoder 사용법
- [ISSUE: FastApi & MongoDB - the full guide #1515](https://github.com/tiangolo/fastapi/issues/1515#issuecomment-782838556)
  + ObjectId 의 wrapper class 생성 (타입 처리)


### 3) mongodb insert_test

#### (1) 간단한 insert_test

일반적인 mongoDB 사용시에는 문제가 안된다. (아리송)

```python
from pymongo.collection import Collection
from pymongo.database import Database

def insert_test(db: Database):
    db.drop_collection("hello")

    coll: Collection = db["hello"]
    # coll.delete_many({})
    coll.insert_one({"id": 1001, "name": "tonyne", "score": 100.5})
    result = coll.insert_many(
        [
            {"id": 1002, "name": "tonyne", "score": 100.5},
            {"id": 1003, "name": "tonyne", "score": 100.5},
            {"id": 1004, "name": "tonyne", "score": 100.5},
            {"id": 1005, "name": "tonyne", "score": 100.5},
        ]
    )
    logger.info(f"_ids = {result.inserted_ids}")
    cusor = coll.find({})
    for doc in cusor:
        logger.info(f"\n{doc}")
    return {"msg": "Hello, Files", "collections": db.list_collection_names()}

"""
api.files:insert_test:45 - _ids = [ObjectId('6340eb861c2cbd9dbb04fe94'), ObjectId('6340eb861c2cbd9dbb04fe95'), ObjectId('6340eb861c2cbd9dbb04fe96'), ObjectId('6340eb861c2cbd9dbb04fe97')]
api.files:insert_test:48 - 
{'_id': ObjectId('6340eb861c2cbd9dbb04fe93'), 'id': 1001, 'name': 'tonyne', 'score': 100.5}
api.files:insert_test:48 - 
{'_id': ObjectId('6340eb861c2cbd9dbb04fe94'), 'id': 1002, 'name': 'tonyne', 'score': 100.5}
api.files:insert_test:48 - 
{'_id': ObjectId('6340eb861c2cbd9dbb04fe95'), 'id': 1003, 'name': 'tonyne', 'score': 100.5}
api.files:insert_test:48 - 
{'_id': ObjectId('6340eb861c2cbd9dbb04fe96'), 'id': 1004, 'name': 'tonyne', 'score': 100.5}
api.files:insert_test:48 - 
{'_id': ObjectId('6340eb861c2cbd9dbb04fe97'), 'id': 1005, 'name': 'tonyne', 'score': 100.5}
"""    
```

#### (2) insert_test 실행시 mongodb 로그

```bash
smp-mongo  | {"t":{"$date":"2022-10-08T03:46:11.600+00:00"},"s":"I",  "c":"COMMAND",  "id":518070,  "ctx":"conn5","msg":"CMD: drop","attr":{"namespace":"tutorial.hello"}}
smp-mongo  | {"t":{"$date":"2022-10-08T03:46:11.604+00:00"},"s":"I",  "c":"STORAGE",  "id":20320,   "ctx":"conn5","msg":"createCollection","attr":{"namespace":"tutorial.hello","uuidDisposition":"generated","uuid":{"uuid":{"$uuid":"c7bb4a7f-314c-4751-80ab-463cb6105f9c"}},"options":{}}}
smp-mongo  | {"t":{"$date":"2022-10-08T03:46:11.610+00:00"},"s":"I",  "c":"INDEX",    "id":20345,   "ctx":"conn5","msg":"Index build: done building","attr":{"buildUUID":null,"collectionUUID":{"uuid":{"$uuid":"c7bb4a7f-314c-4751-80ab-463cb6105f9c"}},"namespace":"tutorial.hello","index":"_id_","ident":"index-1--6041161298439540684","collectionIdent":"collection-0--6041161298439540684","commitTimestamp":null}}
```