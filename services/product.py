from flask import request, current_app, redirect, Response  # <-- Asegúrate de que 'redirect' esté aquí
from bson import json_util
from bson import ObjectId
from config.mongodb import mongo

def create_product_service():
    # Detecta si los datos vienen del formulario web o de una petición API JSON
    if request.form:
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        stock = int(request.form.get('stock', 0))
        category = request.form.get('category')
        image_url = request.form.get('image_url')
    else:
        data = request.get_json() or {}
        name = data.get('name', None)
        description = data.get('description', None)
        price = float(data.get('price', 0))
        stock = int(data.get('stock', 0))
        category = data.get('category', None)
        image_url = data.get('image_url', None)

    # Validación con tu mismo estilo 'if title:'
    if name:
        with current_app.app_context():
            # Inserta ordenadamente en la colección específica 'products'
            mongo.db.products.insert_one({
                'name': name,
                'description': description,
                'price': price,
                'stock': stock,
                'category': category,
                'image_url': image_url
            })
        
        # Criterio de aceptación: Redirigir a la lista si se registró usando la web
        if request.form:
            return redirect('/products/')
        
        return {'message': 'Product registered successfully'}, 201
    else:
        return 'invalid payload', 400

def get_products_service():
    with current_app.app_context():
        data = mongo.db.products.find()
        result = json_util.dumps(data)
        return Response(result, mimetype='application/json')

def get_product_by_id_service(id):
    with current_app.app_context():
        try:
            # CORREGIDO: Todo el bloque try/except ahora tiene los 4 espacios de indentación obligatorios hacia la derecha
            product = mongo.db.products.find_one({'_id': ObjectId(id)})
            return product
        except Exception as e:
            print(f"Error al buscar el producto: {e}")
            return None

# Añade esto en services/product.py para uso de las vistas HTML
def get_products_list_service():
    with current_app.app_context():
        # Trae todos los productos de la base de datos
        return list(mongo.db.products.find())

def update_product_service(id):
    from flask import request, redirect
    with current_app.app_context():
        try:
            # Obtener los datos del formulario enviado
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price', 0))
            stock = int(request.form.get('stock', 0))
            category = request.form.get('category')
            image_url = request.form.get('image_url')

            # Actualizar el documento en MongoDB filtrando por su ObjectId
            mongo.db.products.update_one(
                {'_id': ObjectId(id)},
                {
                    '$set': {
                        'name': name,
                        'description': description,
                        'price': price,
                        'stock': stock,
                        'category': category,
                        'image_url': image_url
                    }
                }
            )
            # Al terminar correctamente, redirige al detalle del producto o inventario
            return redirect(f'/products/{id}')
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
            return "Error interno al actualizar el producto", 500