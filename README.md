# Tienda de Electrodomésticos DB

Aplicación web desarrollada con **Python Flask** y **MongoDB** para la gestión de productos de una tienda de electrodomésticos.  
El sistema permite registrar, visualizar, editar y eliminar productos, además de organizarlos por categorías como electrodomésticos, cómputo y celulares.

## Descripción del proyecto

Este proyecto consiste en una tienda web básica orientada a la administración de productos tecnológicos y electrodomésticos.  
La aplicación utiliza Flask como framework backend y MongoDB como base de datos NoSQL para almacenar la información de los productos.

Cada producto puede registrar los siguientes datos:

- Nombre del producto
- Descripción
- Precio
- Stock disponible
- Categoría
- Imagen del producto

Además, el sistema permite cargar imágenes desde un formulario y almacenarlas dentro de la carpeta `static/uploads`.

## Tecnologías utilizadas

- Python
- Flask
- MongoDB
- Flask-PyMongo
- HTML
- CSS
- Jinja2 Templates
- Werkzeug

## Estructura del proyecto

```txt
eltrodomesticosDB/
│
├── app.py
├── config/
├── routes/
├── services/
├── static/
│   └── uploads/
├── templates/
└── python-flask-mongodb-api/

Funcionalidades principales
Gestión de productos

El sistema permite realizar operaciones básicas sobre los productos:

Listar todos los productos registrados.
Registrar nuevos productos.
Ver el detalle de un producto.
Editar la información de un producto.
Eliminar productos de la base de datos.
Gestión por categorías

Los productos pueden visualizarse por categorías:

Electrodomésticos
Cómputo
Celulares

Carga de imágenes
static/uploads/

Requisitos previos

Antes de ejecutar el proyecto, se debe tener instalado:

Python 3.x
MongoDB
pip
Git

También se recomienda usar un entorno virtual para instalar las dependencias del proyecto.

La aplicación permite subir imágenes de productos desde el formulario de registro o edición.
Instalación y ejecución
1. Clonar el repositorio
git clone https://github.com/josevargasv-blip/eltrodomesticosDB.git

2. Ingresar a la carpeta del proyecto
cd eltrodomesticosDB

3. Crear un entorno virtual
En Windows:
python -m venv venv

4. Activar el entorno virtual

En Windows PowerShell:
venv\Scripts\activate

5. Instalar dependencias
pip install flask flask-pymongo pymongo werkzeug

6. Verificar que MongoDB esté ejecutándose
La aplicación se conecta a MongoDB mediante la siguiente URI:

7. Ejecutar la aplicación
python app.py

La aplicación se ejecutará en:
http://localhost:5000

Objetivo del proyecto

El objetivo del proyecto es implementar una aplicación web funcional para administrar productos de una tienda de electrodomésticos, aplicando conexión con base de datos MongoDB, manejo de formularios, carga de imágenes y operaciones CRUD.

Posibles mejoras futuras
Agregar autenticación para administrador.
Implementar carrito de compras.
Añadir búsqueda de productos por nombre.
Mejorar la validación de formularios.
Separar completamente la lógica en rutas, servicios y configuración.
Agregar paginación para grandes cantidades de productos.
Implementar una API REST para consumo externo.
Autor

Proyecto desarrollado para una tienda de electrodomésticos como práctica de integración entre Flask y MongoDB.
