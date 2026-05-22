from flask import Flask, render_template
from dotenv import load_dotenv
from routes.todo import todo
from pymongo import MongoClient
from config.mongodb import mongo

# Cargamos las variables de entorno
load_dotenv()

app = Flask(__name__)

# --- CONFIGURACIÓN DE PYMONGO ---
app.config["MONGO_URI"] = "mongodb+srv://josevargasv_db_user:QAQvbESFsqQAVJt8@cluster0.gksmom6.mongodb.net/ApoloDatabase?retryWrites=true&w=majority&appName=Cluster0"
mongo.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(todo, url_prefix='/todos')

if __name__ == '__main__':
    try:
        check_client = MongoClient(app.config["MONGO_URI"])
        check_client.admin.command('ping')
        print("¡Conexión exitosa a MongoDB Atlas!")
        check_client.close()  
    except Exception as e:
        print("Error al conectar a MongoDB:", e)

    app.run(debug=True, use_reloader=False)