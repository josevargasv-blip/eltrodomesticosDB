from flask import Blueprint, render_template, request, redirect
from services.product import (
    create_product_service,
    get_products_list_service,
    get_product_by_id_service,
    update_product_service
)

product_blueprint = Blueprint('product', __name__)

# 1. PANEL PRINCIPAL
@product_blueprint.route('/products', methods=['GET'])
def list_products():
    # Llamamos al servicio que ya tiene la lógica de búsqueda y filtros dinámicos
    from services.product import get_products_list_service
    products = get_products_list_service()
    
    # Enviamos los productos filtrados a tu plantilla HTML
    return render_template('products_list.html', products=products)

# 2. HU-01: Formulario para añadir nuevos productos
@product_blueprint.route('/create', methods=['GET'])
def render_create_form():
    return render_template('products_new.html')

# 3. HU-01: Procesa el formulario de guardado
@product_blueprint.route('/new', methods=['POST'])
def save_product():
    return create_product_service()

# 4. HU-02: Vista de detalle de un producto específico
@product_blueprint.route('/<id>', methods=['GET'])
def product_detail_view(id):
    product = get_product_by_id_service(id)
    if product:
        return render_template('product_detail.html', product=product)
    return "Producto no encontrado", 404

# 5. HU-04: Formulario de edición con datos cargados
@product_blueprint.route('/<id>/edit', methods=['GET'])
def edit_product_view(id):
    product = get_product_by_id_service(id)
    if product:
        return render_template('products_edit.html', product=product)
    return "Producto no encontrado", 404

# 6. HU-04: Guarda los cambios del formulario
@product_blueprint.route('/<id>/edit', methods=['POST'])
def update_product(id):
    return update_product_service(id)