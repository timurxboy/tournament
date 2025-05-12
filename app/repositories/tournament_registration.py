from fastapi import HTTPException
from sqlalchemy import select, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.player import Player
from app.models.tournament import Tournament
from app.models.registration_card import RegistrationCard
from app.schemas.tournament import PlayerRegister, PlayerResponse


class TournamentRegisterRepo:
    @classmethod
    async def register(
        cls, db: AsyncSession, tournament_id: int, player: PlayerRegister
    ) -> PlayerResponse:
        tournament_query = (
            select(
                Tournament.id,
                Tournament.name,
                Tournament.max_players,
                Tournament.start_at,
                func.count(RegistrationCard.id).label("registered_players"),
            )
            .outerjoin(
                RegistrationCard, Tournament.id == RegistrationCard.tournament_id
            )
            .where(Tournament.id == tournament_id)
            .group_by(Tournament.id)
        )

        result = await db.execute(tournament_query)
        tournament = result.fetchone()

        # Проверяем есть ли турний с такой id
        if not tournament:
            raise HTTPException(status_code=404, detail="Tournament not found")

        # Проверяем не заполнен ли турнир
        if tournament.registered_players >= tournament.max_players:
            raise HTTPException(status_code=400, detail="Max players limit reached")

        # Попытка найти уже существующего игрока
        existing_player_query = select(Player).where(Player.email == player.email)
        result = await db.execute(existing_player_query)
        existing_player = result.scalar_one_or_none()

        if existing_player:
            player_id = existing_player.id
        else:
            # Создаем нового игрока
            player_query = (
                insert(Player)
                .values(name=player.name, email=player.email)
                .returning(Player.id)
            )
            result = await db.execute(player_query)
            player_id = result.scalar_one()

        # Проверяем, не зарегистрирован ли уже игрок на этот турнир
        check_query = select(RegistrationCard).where(
            RegistrationCard.tournament_id == tournament_id,
            RegistrationCard.player_id == player_id,
        )
        result = await db.execute(check_query)
        existing_registration = result.scalar_one_or_none()

        if existing_registration:
            raise HTTPException(
                status_code=400,
                detail="The player is already registered for this tournament",
            )

        # Регистрируем игрока
        reg_query = insert(RegistrationCard).values(
            tournament_id=tournament_id, player_id=player_id
        )
        await db.execute(reg_query)

        result = await db.execute(tournament_query)
        tournament = result.fetchone()

        await db.commit()

        if not tournament:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error retrieving tournament data after registration",
            )

        return PlayerResponse(
            id=tournament.id,
            name=tournament.name,
            max_players=tournament.max_players,
            start_at=tournament.start_at,
            registered_players=tournament.registered_players,
        )
