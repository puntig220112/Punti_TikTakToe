from BACKEND_NAME_PLACEHOLDER.api._app import build_app
from BACKEND_NAME_PLACEHOLDER.api._routes import get_engine
from BACKEND_NAME_PLACEHOLDER.model import Base
from sqlalchemy import create_engine
from fastapi.testclient import TestClient

engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)

app = build_app()
app.dependency_overrides[get_engine] = lambda: engine

with TestClient(app) as c:
    c.post('/users', json={'user_name':'a', 'password':'b','first_name':'c','last_name':'d'})
    g = c.post('/games', json={'player_name':'a'}).json()
    gid = g['id']
    print('Move 1:', c.put(f'/games/{gid}/move/1?char=X').status_code)
    print('Move 2:', c.put(f'/games/{gid}/move/2?char=X').status_code)
    print('Move 3 (O):', c.put(f'/games/{gid}/move/2?char=O').status_code)
