from fastapi import FastAPI, HTTPException, Depends
from typing import List

from BACKEND_NAME_PLACEHOLDER.engine import get_engine
from BACKEND_NAME_PLACEHOLDER.schema._game import GameCreate, GameResponse
from BACKEND_NAME_PLACEHOLDER.schema._user import UserCreate, UserResponse
from BACKEND_NAME_PLACEHOLDER.crud._game_crud import GameCrud
from BACKEND_NAME_PLACEHOLDER.crud._crud import Crud
from BACKEND_NAME_PLACEHOLDER.utils._tictactoe_logic import check_win

def define_routes(app: FastAPI) -> None:
    engine = get_engine()
    game_crud = GameCrud(engine)
    user_crud = Crud(engine)

    @app.get("/")
    def get_root():
        return {"message": "TicTacToe API"}

    # --- User Endpoints ---

    @app.post("/users", response_model=UserResponse)
    def create_user(user: UserCreate):
        try:
            return user_crud.create_user(user)
        except Exception:
            # Fängt z.B. doppelte Usernames ab
            raise HTTPException(status_code=400, detail="User could not be created. Username might be taken.")

    @app.get("/users", response_model=List[UserResponse])
    def get_users():
        return user_crud.get_users()

    # --- Game Endpoints ---

    @app.post("/games", response_model=GameResponse)
    def create_game(game: GameCreate):
        return game_crud.create_game(game)
        
    @app.get("/games", response_model=List[GameResponse])
    def get_games():
        return game_crud.get_all_games()
        
    @app.get("/games/{game_id}", response_model=GameResponse)
    def get_game(game_id: int):
        game = game_crud.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game
        
    @app.put("/games/{game_id}/move/{position}", response_model=GameResponse)
    def make_move(game_id: int, position: int, char: str):
        if position < 1 or position > 9:
            raise HTTPException(status_code=400, detail="Invalid position")
        if char not in ['X', 'O']:
            raise HTTPException(status_code=400, detail="Invalid char")
            
        game = game_crud.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        if game.status != "ongoing":
            raise HTTPException(status_code=400, detail="Game finished")
            
        index = position - 1
        if game.board[index] != ' ':
            raise HTTPException(status_code=400, detail="Position taken")
            
        new_board = list(game.board)
        new_board[index] = char
        game.board = "".join(new_board)
        
        status = check_win(game.board)
        if status in ['X', 'O']:
            game.status = f"{status.lower()}_won"
        elif status == 'draw':
            game.status = 'draw'
            
        return game_crud.update_game(game)
