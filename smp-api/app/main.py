import uvicorn

from api import hero_router, team_router
from core import app

app.include_router(hero_router)
app.include_router(team_router)


@app.get("/")
def hello():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
