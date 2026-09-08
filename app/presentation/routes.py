from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.business.product_service import ProductService
from app.data.product_repository import SqlAlchemyProductRepository


web_bp = Blueprint("web", __name__)


def product_service() -> ProductService:
    return ProductService(SqlAlchemyProductRepository())


@web_bp.get("/")
def index():
    service = product_service()
    products = service.list_products()
    inventory_value = service.calculate_inventory_value(products)
    return render_template(
        "products/index.html",
        products=products,
        inventory_value=inventory_value,
    )


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


@web_bp.post("/products/<int:product_id>/restock")
def restock_product(product_id):
    try:
        product = product_service().restock_product(
            product_id,
            request.form.get("quantity", ""),
        )
        if product is None:
            flash("Producto no encontrado.", "error")
        else:
            flash("Stock reabastecido correctamente.", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("web.index"))


@web_bp.post("/products/<int:product_id>/discount")
def apply_discount(product_id):
    try:
        product = product_service().apply_discount(
            product_id,
            request.form.get("percentage", ""),
        )
        if product is None:
            flash("Producto no encontrado.", "error")
        else:
            flash("Descuento aplicado correctamente.", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("web.index"))


@web_bp.post("/calculate-tax")
def calculate_tax():
    try:
        price_with_tax = product_service().calculate_price_with_tax(
            request.form.get("price", ""),
            request.form.get("tax_rate", "18"),
        )
        flash(f"Precio con IGV: S/ {price_with_tax:.2f}", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("web.index"))
