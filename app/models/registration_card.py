from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.db import Base


class RegistrationCard(Base):
    __tablename__ = "registration_card"

    id = Column(Integer, primary_key=True)
    tournament_id = Column(
        Integer, ForeignKey("tournament.id", onupdate="CASCADE"), nullable=False
    )
    player_id = Column(
        Integer, ForeignKey("player.id", onupdate="CASCADE"), nullable=False
    )
    registered_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    tournament = relationship("Tournament", back_populates="registration_cards")
    player = relationship("Player", back_populates="registration_cards")
