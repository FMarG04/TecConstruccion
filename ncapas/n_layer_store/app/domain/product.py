from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Product:
    id: Optional[int]
    name: str
    price: Decimal
    stock: int
    created_at: Optional[datetime] = None

    def validate(self) -> None:
        if not self.name:
            raise ValueError("El nombre del producto es obligatorio.")
        if self.price <= Decimal("0"):
            raise ValueError("El precio debe ser mayor que cero.")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")
