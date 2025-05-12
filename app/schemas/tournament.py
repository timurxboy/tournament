from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class TournamentCreate(BaseModel):
    name: str
    max_players: int = Field(..., ge=2)
    start_at: datetime


class TournamentResponse(BaseModel):
    id: int
    name: str
    max_players: int
    start_at: datetime

    class Config:
        from_attributes = True


class PlayerRegister(BaseModel):
    name: str
    email: EmailStr


class PlayerResponse(BaseModel):
    id: int
    name: str
    max_players: int
    start_at: datetime
    registered_players: int

    class Config:
        from_attributes = True
