from flask import Flask, render_template
from dotenv import load_dotenv
from routes.todo import todo
from routes.product import product_blueprint
from config.mongodb import mongo

# Cargamos las variables de entorno
load_dotenv()

app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS LOCAL ---
# Usamos localhost para evadir los problemas de certificados SSL/TLS de la red local
app.config["MONGO_URI"] = "mongodb://localhost:27017/ApoloDatabase"

# Inicializamos la extensión de PyMongo de forma estándar
mongo.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

# Registro de las rutas de tus módulos (Todos y Productos)
app.register_blueprint(todo, url_prefix='/todos')
app.register_blueprint(product_blueprint, url_prefix='/products')

if __name__ == '__main__':
    print("¡Servidor Flask Iniciado Correctamente en Modo Local!")
    app.run(debug=True, use_reloader=False)