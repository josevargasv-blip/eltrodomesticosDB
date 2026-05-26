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