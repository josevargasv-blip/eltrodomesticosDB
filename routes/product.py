from flask import Blueprint, render_template
from services.product import create_product_service, get_products_service

product_blueprint = Blueprint('product', __name__)

# GET /products/ -> Muestra el inventario en formato JSON
@product_blueprint.route('/', methods=['GET'])
def list_products():
    return get_products_service()

# GET /products/new -> Abre el hermoso formulario oscuro que armamos
@product_blueprint.route('/new', methods=['GET'])
def new_product_view():
    return render_template('products_new.html')

# POST /products/new -> Recibe los datos del formulario y los guarda en MongoDB
@product_blueprint.route('/new', methods=['POST'])
def save_product():
    return create_product_service()

# GET /products/<id> -> Abre la vista de detalle de un producto específico
@product_blueprint.route('/<id>', methods=['GET'])
def product_detail_view(id):
    from services.product import get_product_by_id_service
    # Obtenemos el producto desde el servicio
    product = get_product_by_id_service(id)

    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Producto no encontrado", 404

# GET /products/<id>/edit -> Abre el formulario de edición con los datos cargados
@product_blueprint.route('/<id>/edit', methods=['GET'])
def edit_product_view(id):
    from services.product import get_product_by_id_service
    # Reutilizamos el servicio de la HU-04 para obtener los datos actuales
    product = get_product_by_id_service(id)
    if product:
        return render_template('products_edit.html', product=product)
    else:
        return "Producto no encontrado", 404

# POST /products/<id>/edit -> Procesa los cambios del formulario y actualiza MongoDB
@product_blueprint.route('/<id>/edit', methods=['POST'])
def update_product(id):
    from services.product import update_product_service
    return update_product_service(id)