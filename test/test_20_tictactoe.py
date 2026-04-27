import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from BACKEND_NAME_PLACEHOLDER.config import Config
from BACKEND_NAME_PLACEHOLDER.api._app import build_app
from BACKEND_NAME_PLACEHOLDER.utils._tictactoe_logic import check_win
from BACKEND_NAME_PLACEHOLDER.schema._game import GameCreate, GameResponse
from BACKEND_NAME_PLACEHOLDER.schema._user import UserCreate
from BACKEND_NAME_PLACEHOLDER.model import Base
from BACKEND_NAME_PLACEHOLDER.crud._game_crud import GameCrud
from BACKEND_NAME_PLACEHOLDER.crud._crud import Crud

# --- 1-4: LOGIK TESTS ---
def test_01_win_ongoing():
    assert check_win("         ") == "ongoing"

def test_02_win_row():
    assert check_win("XXX      ") == "X"

def test_03_win_diag():
    assert check_win("X   X   X") == "X"

def test_04_win_draw():
    assert check_win("XOXOXXOXO") == "draw"


# --- 5-7: SCHEMA TESTS ---
def test_05_game_create_schema():
    assert GameCreate(player_name="User1").player_name == "User1"

def test_06_game_response_schema():
    assert GameResponse(id=1, player_x="User1", board="         ", status="ongoing").id == 1

def test_07_user_create_schema():
    assert UserCreate(user_name="User1", password="123", first_name="Vor", last_name="Nach").user_name == "User1"


# --- 8-12: DATENBANK (CRUD) TESTS ---
@pytest.fixture
def engine():
    # Erstellt eine leere Datenbank im RAM für diese Tests
    eng = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(eng)
    return eng

def test_08_crud_create_user(engine):
    crud = Crud(engine)
    user = crud.create_user(UserCreate(user_name="u1", password="pw", first_name="A", last_name="B"))
    assert user.user_name == "u1"

def test_09_crud_get_users(engine):
    crud = Crud(engine)
    crud.create_user(UserCreate(user_name="u1", password="pw", first_name="A", last_name="B"))
    assert len(crud.get_users()) == 1

def test_10_crud_create_game(engine):
    g_crud = GameCrud(engine)
    game = g_crud.create_game(GameCreate(player_name="u1"))
    assert game.player_x == "u1"

def test_11_crud_get_games(engine):
    g_crud = GameCrud(engine)
    g_crud.create_game(GameCreate(player_name="u1"))
    assert len(g_crud.get_all_games()) == 1

def test_12_crud_update_game(engine):
    g_crud = GameCrud(engine)
    game = g_crud.create_game(GameCreate(player_name="u1"))
    game.board = "X        "
    upd = g_crud.update_game(game)
    assert upd.board == "X        "


# --- 13-20: WEB SERVER (API) TESTS ---
@pytest.fixture
def client():
    import BACKEND_NAME_PLACEHOLDER.api._app as app_module
    import BACKEND_NAME_PLACEHOLDER.api._routes as routes_module
    from sqlalchemy import create_engine
    from sqlalchemy.pool import StaticPool
    from BACKEND_NAME_PLACEHOLDER.model import Base

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)

    original_get_engine = routes_module.get_engine
    routes_module.get_engine = lambda: engine

    app_module._app = None
    app = app_module.build_app()

    with TestClient(app) as test_client:
        yield test_client

    routes_module.get_engine = original_get_engine


def test_13_api_root(client):
    assert client.get("/").status_code == 200

def test_14_api_create_user(client):
    resp = client.post("/users", json={"user_name": "api_u", "password": "123", "first_name": "F", "last_name": "L"})
    assert resp.status_code == 200

def test_15_api_get_users(client):
    client.post("/users", json={"user_name": "api_u2", "password": "123", "first_name": "F", "last_name": "L"})
    assert client.get("/users").status_code == 200

def test_16_api_create_game_fail_no_user(client):
    # Testiert unseren Check: Ohne User (den es nicht gibt) schlägt es fehl
    resp = client.post("/games", json={"player_name": "Rando"})
    assert resp.status_code == 404

def test_17_api_create_game_success(client):
    client.post("/users", json={"user_name": "api_u3", "password": "123", "first_name": "F", "last_name": "L"})
    assert client.post("/games", json={"player_name": "api_u3"}).status_code == 200

def test_18_api_get_game(client):
    client.post("/users", json={"user_name": "api_u4", "password": "pw", "first_name": "F", "last_name": "L"})
    g = client.post("/games", json={"player_name": "api_u4"}).json()
    assert client.get(f"/games/{g['id']}").status_code == 200

def test_19_api_make_move_valid(client):
    client.post("/users", json={"user_name": "api_u5", "password": "pw", "first_name": "F", "last_name": "L"})
    g = client.post("/games", json={"player_name": "api_u5"}).json()
    assert client.put(f"/games/{g['id']}/move/1?char=X").status_code == 200

def test_20_api_make_move_invalid_pos(client):
    client.post("/users", json={"user_name": "api_u6", "password": "pw", "first_name": "F", "last_name": "L"})
    g = client.post("/games", json={"player_name": "api_u6"}).json()
    assert client.put(f"/games/{g['id']}/move/10?char=X").status_code == 400