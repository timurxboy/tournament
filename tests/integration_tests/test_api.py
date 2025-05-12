from httpx import AsyncClient
import pytest
from datetime import datetime, timedelta


@pytest.mark.parametrize(
    "name, max_players, start_at, status_code",
    [
        (
            "Test Tournament 1",
            32,
            (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            200,
        ),  # Валидные данные
        (
            "Test Tournament 2",
            6,
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            400,
        ),  # Тест прошедшую дату
        (
            "Test Tournament 3",
            0,
            (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            422,
        ),  # Тест на max_players < 2
    ],
)
async def test_create_tournament(
    name, max_players, start_at, status_code, ac: AsyncClient
):
    response = await ac.post(
        "/tournaments",
        json={"name": name, "max_players": max_players, "start_at": start_at},
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "name, email, tournament_id, status_code",
    [
        ("Test Player 1", "test1@mail.com", 1001, 200),  # Валидные данные
        (
            "Clinton Jacobs",
            "andrew58@hill.com",
            1001,
            200,
        ),  # Валидные данные (существующий email на другой турнир)
        (
            "Dana Jones",
            "smithtimothy@hotmail.com",
            1002,
            400,
        ),  # Тест регистрации дублирующую email
        ("Alice Smith", "alice@example.com", 1018, 400),  # Тест на заполненный турнир
        ("Test Player 2", "test2@mail.com", 100, 404),  # Тест на несуществующий турнир
    ],
)
async def test_register_player(
    name, email, tournament_id, status_code, ac: AsyncClient
):
    resource = await ac.post(
        f"/tournaments/{tournament_id}/register", json={"name": name, "email": email}
    )

    assert resource.status_code == status_code
