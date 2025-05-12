import json
from datetime import datetime

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import Base, async_session_maker, engine

from app.models.tournament import Tournament
from app.models.player import Player
from app.models.registration_card import RegistrationCard

from httpx import AsyncClient, ASGITransport
from app.main import app as fastapi_app


@pytest.fixture(autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mocks_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    tournaments = open_mock_json("tournaments")
    players = open_mock_json("players")
    registration_cards = open_mock_json("registration_cards")

    for tournament in tournaments:
        tournament["start_at"] = datetime.fromisoformat(tournament["start_at"])

    async with async_session_maker() as session:
        add_tournaments = insert(Tournament).values(tournaments)
        add_players = insert(Player).values(players)
        add_registration_cards = insert(RegistrationCard).values(registration_cards)

        await session.execute(add_tournaments)
        await session.execute(add_players)
        await session.execute(add_registration_cards)

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://localhost:8000"
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
