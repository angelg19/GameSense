# models/user_data.py
from pydantic import BaseModel
from typing import Dict, Any, List
from models.hero import HeroData
from models.map import MapData
from models.player import PlayerData
from datetime import datetime

# Define a pydantic model to support our User data type in mongo that holds ranked play profile information
class RankedStatsData(BaseModel):
    total_matches: int
    total_wins: int
    total_assists: int
    total_deaths: int
    total_kills: int
    total_time_played: str
    total_time_played_raw: float
    total_mvp: int
    total_svp: int

    class Config:
        extra = "ignore"

# Define a pydantic model to support our User data type in mongo that holds profile information
class OverallStatsData(BaseModel):
    total_matches: int
    total_wins: int
    ranked: RankedStatsData

    class Config:
        extra = "ignore"

# Define our pydantic model for our User data type in mongo
class UserData(BaseModel):
    name: str
    rivals_uid: float
    player: PlayerData

    # Since you can have no matches played for a given season these stats can all be empty.
    heroes_ranked: List[HeroData] | None = None
    maps: List[MapData] | None = None
    overall_stats: OverallStatsData | None = None
    match_history: List[Any] | None = None

    # Not necessary data, only applies to updates, so it can be handled then.
    is_refresh: bool | None = None
    last_update: datetime | None = None
    

    class Config:
        extra = "ignore"

