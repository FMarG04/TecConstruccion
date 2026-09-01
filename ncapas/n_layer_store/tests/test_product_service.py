import unittest

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


if __name__ == "__main__":
    unittest.main()
