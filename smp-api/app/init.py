from fastapi import FastAPI

from db import create_db_and_tables, engine

app = FastAPI(title="FastAPI + SQLModel + PostgreSQL", version="0.1.0")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
def on_shutdown():
    engine.dispose()
