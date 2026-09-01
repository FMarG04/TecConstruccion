from datetime import datetime

from app.domain.product import Product
from app.infrastructure.database import db


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_domain(self) -> Product:
        return Product(
            id=self.id,
            name=self.name,
            price=self.price,
            stock=self.stock,
            created_at=self.created_at,
        )
