from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_x: Mapped[str] = mapped_column(String(50), nullable=True)
    player_o: Mapped[str] = mapped_column(String(50), nullable=True)
    board: Mapped[str] = mapped_column(String(9), default="         ")
    status: Mapped[str] = mapped_column(String(20), default="ongoing")
