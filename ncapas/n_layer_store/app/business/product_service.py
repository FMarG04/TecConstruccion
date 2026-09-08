from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
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

    def restock_product(self, product_id: int, quantity: str) -> Optional[Product]:
        """Stateful operation: increases the stock of an existing product."""
        try:
            parsed_quantity = int(quantity)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un numero entero.") from None

        if parsed_quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        current = self.repository.get_by_id(product_id)
        if current is None:
            return None

        current.stock += parsed_quantity
        return self.repository.update(product_id, current)

    def apply_discount(self, product_id: int, percentage: str) -> Optional[Product]:
        """Stateful operation: changes the stored price of an existing product."""
        parsed_percentage = self._parse_percentage(percentage)
        current = self.repository.get_by_id(product_id)
        if current is None:
            return None

        current.price = (current.price * (Decimal("1") - parsed_percentage / Decimal("100"))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        current.validate()
        return self.repository.update(product_id, current)

    @staticmethod
    def calculate_inventory_value(products: list[Product]) -> Decimal:
        """Stateless calculation: returns the value without altering products."""
        return sum((product.price * product.stock for product in products), Decimal("0"))

    @staticmethod
    def calculate_price_with_tax(price: str, tax_rate: str = "18") -> Decimal:
        """Stateless calculation: returns a price with tax without persisting it."""
        try:
            parsed_price = Decimal(str(price))
            parsed_tax_rate = Decimal(str(tax_rate))
        except (InvalidOperation, ValueError):
            raise ValueError("El precio y el IGV deben ser numeros validos.") from None

        if parsed_price <= Decimal("0"):
            raise ValueError("El precio debe ser mayor que cero.")
        if parsed_tax_rate < Decimal("0"):
            raise ValueError("El IGV no puede ser negativo.")

        return (parsed_price * (Decimal("1") + parsed_tax_rate / Decimal("100"))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

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

    @staticmethod
    def _parse_percentage(percentage: str) -> Decimal:
        try:
            parsed_percentage = Decimal(str(percentage))
        except (InvalidOperation, ValueError):
            raise ValueError("El descuento debe ser un numero valido.") from None

        if not Decimal("0") < parsed_percentage < Decimal("100"):
            raise ValueError("El descuento debe ser mayor que cero y menor que 100.")
        return parsed_percentage
