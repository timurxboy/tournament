from enum import Enum
from typing import TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class OrderByEnum(Enum):
    ASC = "asc"
    DESC = "desc"


class SortByEnum(Enum):
    ID = "id"
    NAME = "name"


class SPagination(BaseModel):
    page: int
    per_page: int
    order_by: OrderByEnum
    sort_by: SortByEnum

    class Config:
        from_attributes = True


def pagination_params(
    page: int = Query(ge=1, le=500000, required=False, default=1),
    per_page: int = Query(ge=1, le=100, required=False, default=10),
    order_by: OrderByEnum = OrderByEnum.DESC,
    sort_by: SortByEnum = SortByEnum.ID,
) -> SPagination:
    return SPagination(
        page=page, per_page=per_page, order_by=order_by.value, sort_by=sort_by.value
    )
