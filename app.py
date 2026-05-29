import sys
from os import path, makedirs
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

base_dir = path.abspath(path.dirname(__file__))
templates_dir = path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=templates_dir)

# Configuración de carpetas para almacenar fotos físicas
UPLOAD_FOLDER = path.join(base_dir, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not path.exists(UPLOAD_FOLDER):
    makedirs(UPLOAD_FOLDER)

# Conexión a MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/electronicadb"
mongo = PyMongo(app)

# ==========================================
# 1. RUTAS DE VISUALIZACIÓN (CATÁLOGO Y CATEGORÍAS)
# ==========================================

@app.route('/')
def root():
    return redirect('/products')

@app.route('/products')
def get_products():
    """Muestra TODOS los productos registrados"""
    try:
        todos = list(mongo.db.products.find())
        return render_template('products_list.html', productos=todos, categoria_actual='todos')
    except Exception as e:
        return f"Error al conectar con MongoDB: {str(e)}", 500

@app.route('/category/electrodomesticos')
def get_electrodomesticos():
    """Muestra únicamente los Electrodomésticos"""
    try:
        productos = list(mongo.db.products.find({
            'category': {'$in': ['Electrodomésticos', 'Electrodomesticos', 'electrodomesticos']}
        }))
        return render_template('products_list.html', productos=productos, categoria_actual='electrodomesticos')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/category/computo')
def get_computo():
    """Muestra únicamente los productos de Cómputo"""
    try:
        productos = list(mongo.db.products.find({
            'category': {'$in': ['Cómputo', 'Computo', 'computo']}
        }))
        return render_template('products_list.html', productos=productos, categoria_actual='computo')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/category/celulares')
def get_celulares():
    """Muestra únicamente los Celulares"""
    try:
        productos = list(mongo.db.products.find({
            'category': {'$in': ['Celulares', 'celulares']}
        }))
        return render_template('products_list.html', productos=productos, categoria_actual='celulares')
    except Exception as e:
        return f"Error: {str(e)}", 500


# ==========================================
# 2. RUTAS DE CREACIÓN (MASTERS DOUBLE-ROUTE)
# ==========================================

# Mapeamos tanto en singular como en plural para evitar el error "Not Found" por completo
@app.route('/product/create', methods=['GET'])
@app.route('/products/create', methods=['GET'])
def create_product_view():
    """Muestra el formulario para registrar un producto"""
    return render_template('products_new.html')

@app.route('/product/create', methods=['POST'])
@app.route('/products/create', methods=['POST'])
def create_product_store():
    """Procesa el formulario y guarda el producto en MongoDB"""
    try:
        name = request.form.get('name')
        description = request.form.get('description')
        
        price_raw = request.form.get('price', '0')
        price = float(price_raw) if price_raw and price_raw.strip() else 0.0
        
        stock_raw = request.form.get('stock', '0')
        stock = int(stock_raw) if stock_raw and stock_raw.strip() else 0
        
        category = request.form.get('category')
        if not category:
            category = 'Electrodomésticos' 

        image_url = ""
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f"/static/uploads/{filename}"

        if name:
            mongo.db.products.insert_one({
                'name': name,
                'description': description,
                'price': price,
                'stock': stock,
                'category': category,
                'image_url': image_url
            })
            
        return redirect('/products')
    except Exception as e:
        return f"Error interno al guardar: {str(e)}", 500


# ==========================================
# 3. RUTAS DE DETALLE, EDICIÓN Y ELIMINACIÓN
# ==========================================

@app.route('/product/<id>')
@app.route('/products/<id>')
def get_product_detail(id):
    """Muestra la ficha técnica detallada de un producto"""
    try:
        producto = mongo.db.products.find_one({'_id': ObjectId(id)})
        if producto:
            return render_template('products_detail.html', product=producto)
        return "Error: El producto no existe.", 404
    except Exception as e:
        return f"ID no válido: {str(e)}", 400

@app.route('/product/<id>/edit', methods=['GET'])
@app.route('/products/<id>/edit', methods=['GET'])
def edit_product_view(id):
    """Muestra el formulario cargado con los datos actuales para editar"""
    try:
        producto = mongo.db.products.find_one({'_id': ObjectId(id)})
        if producto:
            return render_template('products_edit.html', product=producto)
        return "Error: El producto no existe.", 404
    except Exception as e:
        return f"ID no válido: {str(e)}", 400

@app.route('/product/<id>/edit', methods=['POST'])
@app.route('/products/<id>/edit', methods=['POST'])
def edit_product_update(id):
    """Guarda los cambios editados en la base de datos"""
    try:
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', '0'))
        stock = int(request.form.get('stock', '0'))
        category = request.form.get('category')

        producto_actual = mongo.db.products.find_one({'_id': ObjectId(id)})
        image_url = producto_actual.get('image_url', '') if producto_actual else ''

        if 'image_file' in request.files:
            file = request.files['image_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f"/static/uploads/{filename}"

        mongo.db.products.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': name,
                'description': description,
                'price': price,
                'stock': stock,
                'category': category,
                'image_url': image_url
            }}
        )
        return redirect('/products')
    except Exception as e:
        return f"Error al actualizar: {str(e)}", 400

@app.route('/product/<id>/delete', methods=['POST'])
@app.route('/products/<id>/delete', methods=['POST'])
def delete_product(id):
    """Elimina permanentemente un producto de MongoDB"""
    try:
        mongo.db.products.delete_one({'_id': ObjectId(id)})
        return redirect('/products')
    except Exception as e:
        return f"Error al eliminar: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)