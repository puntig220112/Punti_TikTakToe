from pydantic import BaseModel
from typing import Optional

class GameCreate(BaseModel):
    player_name: str
    password: str

class RemoteGame(BaseModel):
    player_x: str
    player_x_password: str
    player_o: str
    player_o_password: str

class GameResponse(BaseModel):
    id: int
    player_x: Optional[str] = None
    player_o: Optional[str] = None
    board: str
    status: str

    model_config = {
        "from_attributes": True
    }
