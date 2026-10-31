"""Repositorio de órdenes usando SQLAlchemy."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import get_session
from .models import OrderModel
from .schemas import OrderIn, OrderStatus


class SqlOrderRepository:
    """Repositorio de órdenes persistidas en SQLite."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, data: OrderIn) -> OrderModel:
        orden = OrderModel(
            cliente=data.cliente,
            producto=data.producto,
            cantidad=data.cantidad,
            precio_unitario=data.precio_unitario,
            total=data.cantidad * data.precio_unitario,
        )

        self.session.add(orden)
        self.session.commit()
        self.session.refresh(orden)

        return orden

    def get(self, order_id: int) -> OrderModel | None:
        return self.session.get(OrderModel, order_id)

    def list(self, status: OrderStatus | None = None) -> Sequence[OrderModel]:
        consulta = select(OrderModel)

        if status is not None:
            consulta = consulta.where(OrderModel.status == status.value)

        consulta = consulta.order_by(OrderModel.id)

        return self.session.scalars(consulta).all()

    def update(self, order_id: int, data: OrderIn) -> OrderModel | None:
        """Actualiza una orden completa."""
        orden = self.session.get(OrderModel, order_id)

        if orden is None:
            return None

        orden.cliente = data.cliente
        orden.producto = data.producto
        orden.cantidad = data.cantidad
        orden.precio_unitario = data.precio_unitario
        orden.total = data.cantidad * data.precio_unitario

        self.session.commit()
        self.session.refresh(orden)

        return orden

    def update_status(
        self,
        order_id: int,
        status: OrderStatus,
    ) -> OrderModel | None:
        orden = self.session.get(OrderModel, order_id)

        if orden is None:
            return None

        orden.status = status.value

        self.session.commit()
        self.session.refresh(orden)

        return orden

    def delete(self, order_id: int) -> bool:
        orden = self.session.get(OrderModel, order_id)

        if orden is None:
            return False

        self.session.delete(orden)
        self.session.commit()

        return True


def get_repo(
    session: Annotated[Session, Depends(get_session)],
) -> SqlOrderRepository:
    """Crea el repositorio usando la sesión de SQLAlchemy."""
    return SqlOrderRepository(session)