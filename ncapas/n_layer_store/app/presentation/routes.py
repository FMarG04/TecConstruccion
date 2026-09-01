from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.business.product_service import ProductService
from app.data.product_repository import SqlAlchemyProductRepository


web_bp = Blueprint("web", __name__)


def product_service() -> ProductService:
    return ProductService(SqlAlchemyProductRepository())


@web_bp.get("/")
def index():
    products = product_service().list_products()
    return render_template("products/index.html", products=products)


@web_bp.post("/products")
def create_product():
    service = product_service()

    try:
        service.create_product(
            name=request.form.get("name", ""),
            price=request.form.get("price", ""),
            stock=request.form.get("stock", ""),
        )
        flash("Producto creado correctamente.", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("web.index"))


@web_bp.get("/products/<int:product_id>/edit")
def edit_product(product_id):
    product = product_service().get_product(product_id)
    if product is None:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("web.index"))

    return render_template("products/edit.html", product=product)


@web_bp.post("/products/<int:product_id>/edit")
def update_product(product_id):
    service = product_service()

    try:
        product = service.update_product(
            product_id=product_id,
            name=request.form.get("name", ""),
            price=request.form.get("price", ""),
            stock=request.form.get("stock", ""),
        )
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("web.edit_product", product_id=product_id))

    if product is None:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("web.index"))

    flash("Producto actualizado correctamente.", "success")
    return redirect(url_for("web.index"))


@web_bp.post("/products/<int:product_id>/delete")
def delete_product(product_id):
    deleted = product_service().delete_product(product_id)
    if deleted:
        flash("Producto eliminado correctamente.", "success")
    else:
        flash("Producto no encontrado.", "error")

    return redirect(url_for("web.index"))
