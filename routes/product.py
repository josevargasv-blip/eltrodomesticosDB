from flask import Blueprint, render_template, request, redirect
from services.product import (
    create_product_service, 
    get_products_list_service, 
    get_product_by_id_service, 
    update_product_service
)

product_blueprint = Blueprint('product', __name__)

# 1. PANEL PRINCIPAL: Carga el catálogo elegante estilo e-commerce
@product_blueprint.route('/', methods=['GET'])
def list_products():
    products = get_products_list_service()
    return render_template('products_list.html', products=products)

# 2. HU-01: Formulario para añadir nuevos productos (Ruta fija arriba)
@product_blueprint.route('/create', methods=['GET'])
def render_create_form():
    return render_template('products_new.html')

# 3. HU-01: Procesa el formulario de guardado
@product_blueprint.route('/new', methods=['POST'])
def save_product():
    return create_product_service()

# GET /products/<id> -> Vista de detalle
@product_blueprint.route('/<id>', methods=['GET'])
def product_detail_view(id):
    product = get_product_by_id_service(id)
    if product:
        return render_template('product_detail.html', product=product)
    return "Producto no encontrado", 404

# GET /products/<id>/edit -> Formulario de edición
@product_blueprint.route('/<id>/edit', methods=['GET'])
def edit_product_view(id):
    product = get_product_by_id_service(id)
    if product:
        return render_template('products_edit.html', product=product)
    return "Producto no encontrado", 404

# POST /products/<id>/edit -> Guarda los cambios
@product_blueprint.route('/<id>/edit', methods=['POST'])
def update_product(id):
    return update_product_service(id)