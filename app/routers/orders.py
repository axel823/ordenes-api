from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.repository import OrderRepository, get_repo
from app.schemas import OrderIn, OrderOut, OrderStatus

router = APIRouter(prefix="/orders", tags=["orders"])

Repo = Annotated[OrderRepository, Depends(get_repo)]


@router.post(
    "",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    data: OrderIn,
    repo: Repo,
) -> OrderOut:
    return repo.add(data)


@router.get(
    "",
    response_model=list[OrderOut],
)
def list_orders(
    repo: Repo,
    estado: OrderStatus | None = None,
) -> list[OrderOut]:
    return repo.list(estado)


@router.get(
    "/{order_id}",
    response_model=OrderOut,
)
def get_order(
    order_id: int,
    repo: Repo,
) -> OrderOut:
    order = repo.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    return order


@router.put(
    "/{order_id}",
    response_model=OrderOut,
)
def update_order(
    order_id: int,
    data: OrderIn,
    repo: Repo,
) -> OrderOut:
    order = repo.update(order_id, data)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order(
    order_id: int,
    repo: Repo,
) -> None:
    deleted = repo.delete(order_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )
    