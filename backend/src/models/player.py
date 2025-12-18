from pydantic import BaseModel, root_validator

# Define our pydantic model for our Player data type in mongo
class PlayerData(BaseModel):
    name: str
    uid: float
    level: str
    icon: str
    rank: str

    class Config:
        extra = "ignore"
    
    # When creating a new instance of this data type, use a special field to get the rank and icon values.
    @root_validator(pre=True)
    def extract_nested_name(cls, values):
        if "rank" in values and "rank" in values["rank"]:
            values["rank"] = values["rank"]["rank"]
        if "icon" in values and "player_icon" in values["icon"]:
            values["icon"] = values["icon"]["player_icon"]
        return values
