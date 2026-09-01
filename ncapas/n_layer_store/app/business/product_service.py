from decimal import Decimal, InvalidOperation
from typing import Optional, Protocol

from app.domain.product import Product


class ProductRepository(Protocol):
    def list_all(self) -> list[Product]:
        ...

    def get_by_id(self, product_id: int) -> Optional[Product]:
        ...

    def create(self, product: Product) -> Product:
        ...

    def update(self, product_id: int, product: Product) -> Optional[Product]:
        ...

    def delete(self, product_id: int) -> bool:
        ...


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_products(self) -> list[Product]:
        return self.repository.list_all()

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.repository.get_by_id(product_id)

    def create_product(self, name: str, price: str, stock: str) -> Product:
        product = self._build_product(name, price, stock)
        return self.repository.create(product)

    def update_product(
        self,
        product_id: int,
        name: str,
        price: str,
        stock: str,
    ) -> Optional[Product]:
        product = self._build_product(name, price, stock)
        return self.repository.update(product_id, product)

    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete(product_id)

    def _build_product(self, name: str, price: str, stock: str) -> Product:
        try:
            parsed_price = Decimal(str(price))
        except (InvalidOperation, ValueError):
            raise ValueError("El precio debe ser un numero valido.") from None

        try:
            parsed_stock = int(stock)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un numero entero.") from None

        product = Product(
            id=None,
            name=name.strip(),
            price=parsed_price,
            stock=parsed_stock,
        )
        product.validate()
        return product
