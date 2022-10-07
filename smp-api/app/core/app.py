from fastapi import FastAPI

from core.mgdb import get_mongodb
from core.pgdb import create_db_and_tables, engine

app = FastAPI(title="FastAPI + SQLModel + PostgreSQL", version="0.1.0")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    app.mongodb = get_mongodb()


@app.on_event("shutdown")
def on_shutdown():
    engine.dispose()
    app.mongodb.client.close()
    app.mongodb = None
    # get_mongodb().client.close()
