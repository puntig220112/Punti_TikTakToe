from sqlalchemy.orm import Session
from BACKEND_NAME_PLACEHOLDER.model._game import Game
from BACKEND_NAME_PLACEHOLDER.schema._game import GameCreate

class GameCrud:
    def __init__(self, engine):
        self._engine = engine

    def create_game(self, game_data: GameCreate):
        with Session(self._engine) as db:
            new_game = Game(player_x=game_data.player_name, board="         ", status="ongoing")
            db.add(new_game)
            db.commit()
            db.refresh(new_game)
            db.expunge(new_game)
            return new_game
            
    def get_all_games(self):
        with Session(self._engine) as db:
            return db.query(Game).all()

    def get_game(self, game_id: int):
        with Session(self._engine) as db:
            game = db.query(Game).filter(Game.id == game_id).first()
            if game: db.expunge(game)
            return game

    def update_game(self, game: Game):
        with Session(self._engine) as db:
            game_db = db.query(Game).filter(Game.id == game.id).first()
            game_db.board = game.board
            game_db.status = game.status
            db.commit()
            db.refresh(game_db)
            db.expunge(game_db)
            return game_db
