from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, asc, desc, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tournament import Tournament
from app.models.registration_card import RegistrationCard
from app.schemas.pagination import OrderByEnum, SPagination
from app.schemas.tournament import TournamentResponse


class TournamentRepo:
    model = Tournament

    @classmethod
    async def get_all(
        cls,
        db: AsyncSession,
        pagination: SPagination,
        name: Optional[str] = None,
    ):
        order = desc if pagination.order_by == OrderByEnum.DESC else asc

        filters = []
        if name:
            filters.append(cls.model.name == name)

        # Формируем запрос для подсчета общего количества элементов с учетом фильтров и получаем общее количество записей
        total_query = select(func.count()).select_from(cls.model).filter(*filters)
        total_result = await db.execute(total_query)
        total_count = total_result.scalar() or 0

        # Рассчитываем общее количество страниц для пагинации
        total_pages = (total_count + pagination.per_page - 1) // pagination.per_page

        # Формируем основной запрос для получения списка элементов с дополнительным подсчётом зарегистрированных игроков
        query = (
            select(
                cls.model, func.count(RegistrationCard.id).label("registered_players")
            )
            .outerjoin(RegistrationCard)
            .filter(*filters)
            .group_by(cls.model.id)
            .order_by(order(getattr(cls.model, pagination.sort_by.value)))
            .limit(pagination.per_page)
            .offset((pagination.page - 1) * pagination.per_page)
        )

        result = await db.execute(query)
        items = result.all()

        # Преобразуем результаты в список словарей для удобного использования
        values = []
        for tournament, registered_players in items:
            values.append(
                {
                    "id": tournament.id,
                    "name": tournament.name,
                    "max_players": tournament.max_players,
                    "start_at": tournament.start_at,
                    "registered_players": registered_players,
                }
            )

        return {"pages": total_pages, "values": values}

    @classmethod
    async def create(cls, db: AsyncSession, **data):
        query = (
            insert(cls.model)
            .values(**data)
            .returning(
                cls.model.id,
                cls.model.name,
                cls.model.max_players,
                cls.model.start_at,
                cls.model.created_at,
            )
        )

        result = await db.execute(query)
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=500, detail="Failed to create tournament")

        values = dict(row._mapping)

        await db.commit()

        return TournamentResponse(**values)
