from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.tournament import (
    TournamentCreate,
    TournamentResponse,
    PlayerRegister,
    PlayerResponse,
)
from app.schemas.pagination import pagination_params, SPagination
from typing import Annotated, Optional

from app.repositories.tournament_registration import TournamentRegisterRepo
from app.repositories.tournament import TournamentRepo


router = APIRouter(prefix="/tournaments", tags=["Tournaments"])


@router.get("")
async def list_tournaments(
    pagination: Annotated[SPagination, Depends(pagination_params)],
    name: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    return await TournamentRepo.get_all(db=db, pagination=pagination, name=name)


@router.post("")
async def create_tournament(
    request: TournamentCreate, db: AsyncSession = Depends(get_db)
) -> TournamentResponse:
    if request.start_at.astimezone(timezone.utc) <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="start_at must be in the future")

    return await TournamentRepo.create(db=db, **request.dict())


@router.post("/{tournament_id}/register")
async def register_player(
    tournament_id: int, request: PlayerRegister, db: AsyncSession = Depends(get_db)
) -> PlayerResponse:
    return await TournamentRegisterRepo.register(
        db=db, tournament_id=tournament_id, player=request
    )
