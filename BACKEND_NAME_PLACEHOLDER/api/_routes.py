from fastapi import FastAPI, HTTPException, Depends
from typing import List

from BACKEND_NAME_PLACEHOLDER.engine import get_engine
from BACKEND_NAME_PLACEHOLDER.schema._game import GameCreate, GameResponse, RemoteGame
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
            raise HTTPException(status_code=400, detail="User could not be created. Username might be taken.")

    @app.get("/users", response_model=List[UserResponse])
    def get_users():
        return user_crud.get_users()

    # --- Game Endpoints ---

    @app.post("/localgame", response_model=GameResponse)
    def create_game(game: GameCreate):
        all_users = user_crud.get_users()
        user_exists = any(u.user_name == game.player_name and u.password_hash == game.password for u in all_users)
        
        if not user_exists:
            raise HTTPException(status_code=404, detail="Username or password incorrect.")
            
        return game_crud.create_game(game)
    
    @app.post("/remotegame", response_model=GameResponse)
    def create_remote_game(game: RemoteGame):
        all_users = user_crud.get_users()
        user_x_exists = any(u.user_name == game.player_x and u.password_hash == game.player_x_password for u in all_users)
        user_o_exists = any(u.user_name == game.player_o and u.password_hash == game.player_o_password for u in all_users)

        if not user_x_exists:
            raise HTTPException(status_code=404, detail="Player X username or password incorrect.")
        if not user_o_exists:
            raise HTTPException(status_code=404, detail="Player O username or password incorrect.")
        
        return game_crud.create_remote_game(game)


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
    def make_move(game_id: int, position: int, user_name: str, password: str):
        if position < 1 or position > 9:
            raise HTTPException(status_code=400, detail="Invalid position")
            
        game = game_crud.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        if game.status != "ongoing":
            raise HTTPException(status_code=400, detail="Game finished")
            
        index = position - 1
        if game.board[index] != ' ':
            raise HTTPException(status_code=400, detail="Position taken")

        x_count = game.board.count('X')
        o_count = game.board.count('O')
        
        # Automatisch ermitteln wer dran ist
        if x_count > o_count:
            expected_char = 'O'
        else:
            expected_char = 'X'

        # Prüfen ob der richtige User den Zug macht
        if expected_char == 'X':
            if game.player_x != user_name:
                raise HTTPException(status_code=400, detail="It's player X's turn! Wrong username.")
        elif expected_char == 'O':
            # Bei Localgames (wo player_o leer ist), muss zumindest einer existieren. 
            # Aber bei Remotegames muss er exakt passen!
            if game.player_o is not None and game.player_o != user_name:
                raise HTTPException(status_code=400, detail="It's player O's turn! Wrong username.")

        # Passwort-Check in der Datenbank
        all_users = user_crud.get_users()
        user_valid = any(u.user_name == user_name and u.password_hash == password for u in all_users)
        
        if not user_valid:
            raise HTTPException(status_code=404, detail="Username or password incorrect.")
            
        new_board = list(game.board)
        new_board[index] = expected_char
        game.board = "".join(new_board)
        
        status = check_win(game.board)
        if status in ['X', 'O']:
            game.status = f"{status.lower()}_won"
        elif status == 'draw':
            game.status = 'draw'
            
        return game_crud.update_game(game)
