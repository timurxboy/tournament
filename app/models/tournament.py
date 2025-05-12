from sqlalchemy import Column, Integer, String, TIMESTAMP, text, CheckConstraint
from sqlalchemy.orm import relationship

from app.db import Base


class Tournament(Base):
    __tablename__ = "tournament"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)
    max_players = Column(Integer, nullable=False)
    start_at = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    registration_cards = relationship("RegistrationCard", back_populates="tournament")

    __table_args__ = (
        CheckConstraint("max_players > 1", name="check_max_players_positive"),
    )
