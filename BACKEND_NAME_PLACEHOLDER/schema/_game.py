from pydantic import BaseModel
from typing import Optional

class GameCreate(BaseModel):
    player_name: str

class GameResponse(BaseModel):
    id: int
    player_x: Optional[str] = None
    player_o: Optional[str] = None
    board: str
    status: str

    model_config = {
        "from_attributes": True
    }
