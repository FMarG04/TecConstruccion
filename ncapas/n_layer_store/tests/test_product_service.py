import unittest
from decimal import Decimal

from app.business.product_service import ProductService


class FakeProductRepository:
    def __init__(self):
        self.products = []

    def list_all(self):
        return self.products

    def get_by_id(self, product_id):
        return next((product for product in self.products if product.id == product_id), None)

    def create(self, product):
        product.id = len(self.products) + 1
        self.products.append(product)
        return product

    def update(self, product_id, product):
        current = self.get_by_id(product_id)
        if current is None:
            return None

        current.name = product.name
        current.price = product.price
        current.stock = product.stock
        return current

    def delete(self, product_id):
        current = self.get_by_id(product_id)
        if current is None:
            return False

        self.products.remove(current)
        return True


class ProductServiceTest(unittest.TestCase):
    def setUp(self):
        self.repository = FakeProductRepository()
        self.service = ProductService(self.repository)

    def test_creates_valid_product(self):
        product = self.service.create_product("Mouse", "35.50", "8")

        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Mouse")
        self.assertEqual(product.stock, 8)

    def test_rejects_empty_name(self):
        with self.assertRaisesRegex(ValueError, "nombre"):
            self.service.create_product("", "35.50", "8")

    def test_rejects_negative_stock(self):
        with self.assertRaisesRegex(ValueError, "stock"):
            self.service.create_product("Mouse", "35.50", "-1")

    def test_restock_increases_existing_product_stock(self):
        product = self.service.create_product("Mouse", "35.50", "8")

        updated = self.service.restock_product(product.id, "5")

        self.assertEqual(updated.stock, 13)

    def test_discount_changes_existing_product_price(self):
        product = self.service.create_product("Mouse", "100", "8")

        updated = self.service.apply_discount(product.id, "15")

        self.assertEqual(updated.price, Decimal("85.00"))

    def test_inventory_value_does_not_change_products(self):
        first = self.service.create_product("Mouse", "35.50", "2")
        second = self.service.create_product("Teclado", "50", "3")

        value = self.service.calculate_inventory_value([first, second])

        self.assertEqual(value, Decimal("221.00"))
        self.assertEqual(first.stock, 2)
        self.assertEqual(second.price, Decimal("50"))

    def test_calculates_price_with_tax_without_persisting_it(self):
        price_with_tax = self.service.calculate_price_with_tax("100", "18")

        self.assertEqual(price_with_tax, Decimal("118.00"))


if __name__ == "__main__":
    unittest.main()
