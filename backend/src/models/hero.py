# models/hero.py
from pydantic import BaseModel

# Define a pydantic model to support our Hero data type in mongo that holds attack information
class MainAttackData(BaseModel):
    hits: int
    total: int

    class Config:
        extra = "ignore"

# Define our pydantic model for our Hero data type in mongo
class HeroData(BaseModel):
    hero_name: str
    matches: int
    wins: int
    kills: int
    deaths: int
    assists: int
    mvp: int
    svp: int
    play_time: float
    damage: float
    heal: float
    damage_taken: float
    main_attack: MainAttackData

    class Config:
        extra = "ignore"