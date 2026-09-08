from typing import Optional

from app.data.models import ProductModel
from app.domain.product import Product
from app.infrastructure.database import db


class SqlAlchemyProductRepository:
    def list_all(self) -> list[Product]:
        rows = ProductModel.query.order_by(ProductModel.created_at.desc()).all()
        return [row.to_domain() for row in rows]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        row = db.session.get(ProductModel, product_id)
        if row is None:
            return None
        return row.to_domain()

    def create(self, product: Product) -> Product:
        row = ProductModel(
            name=product.name,
            price=product.price,
            stock=product.stock,
        )
        db.session.add(row)
        db.session.commit()
        return row.to_domain()

    def update(self, product_id: int, product: Product) -> Optional[Product]:
        row = db.session.get(ProductModel, product_id)
        if row is None:
            return None

        row.name = product.name
        row.price = product.price
        row.stock = product.stock
        db.session.commit()
        return row.to_domain()

    def delete(self, product_id: int) -> bool:
        row = db.session.get(ProductModel, product_id)
        if row is None:
            return False

        db.session.delete(row)
        db.session.commit()
        return True
