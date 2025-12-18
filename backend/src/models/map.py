from pydantic import BaseModel

# Define our pydantic model for our maps data type in mongo
class MapData(BaseModel):
    map_id: int
    matches: int
    wins : int
    kills: int
    deaths: int
    assists: int
    play_time: float

    class Config:
        extra = "ignore"