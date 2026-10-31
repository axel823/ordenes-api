"""Rutas de la API de órdenes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..repository_sql import SqlOrderRepository, get_repo
from ..schemas import OrderIn, OrderOut, OrderStatus

router = APIRouter(prefix="/orders", tags=["Órdenes"])

Repo = Annotated[SqlOrderRepository, Depends(get_repo)]


@router.post(
    "",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
)
def crear_orden(data: OrderIn, repo: Repo) -> OrderOut:
    """Crea una nueva orden."""
    return repo.add(data)


@router.get("", response_model=list[OrderOut])
def listar_ordenes(
    repo: Repo,
    status: OrderStatus | None = None,
) -> list[OrderOut]:
    """Lista todas las órdenes, con filtro opcional por estado."""
    return list(repo.list(status))


@router.get("/{order_id}", response_model=OrderOut)
def obtener_orden(order_id: int, repo: Repo) -> OrderOut:
    """Obtiene una orden por su ID."""
    orden = repo.get(order_id)

    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    return orden


@router.put("/{order_id}", response_model=OrderOut)
def actualizar_orden(
    order_id: int,
    data: OrderIn,
    repo: Repo,
) -> OrderOut:
    """Actualiza una orden completa."""
    orden = repo.update(order_id, data)

    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    return orden


@router.patch("/{order_id}/status", response_model=OrderOut)
def actualizar_estado(
    order_id: int,
    status: OrderStatus,
    repo: Repo,
) -> OrderOut:
    """Actualiza el estado de una orden."""
    orden = repo.update_status(order_id, status)

    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    return orden


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_orden(order_id: int, repo: Repo) -> None:
    """Elimina una orden."""
    if not repo.delete(order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )
    