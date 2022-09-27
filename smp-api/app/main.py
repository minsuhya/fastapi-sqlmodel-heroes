from typing import List

import uvicorn

# from fastapi import Depends, HTTPException, Query, status
from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select

from db import get_session
from init import app
from models import Hero, HeroCreate, HeroRead, HeroUpdate


@app.get("/heroes/", response_model=List[HeroRead])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.post("/heroes/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(hero_id: int, *, session: Session = Depends(get_session), hero: HeroUpdate):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, *, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return {"ok": True}


@app.get("/hero/{id}", response_model=HeroRead)
def get_hero(id: int, *, session: Session = Depends(get_session)):
    hero = session.exec(select(Hero).where(Hero.id == id)).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
