from flask import request, render_template, current_app, redirect
from bson import ObjectId
from werkzeug.utils import secure_filename
from config.mongodb import mongo
import os
import re


def get_products_service():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    precio_min = request.args.get("precio_min", "").strip()
    precio_max = request.args.get("precio_max", "").strip()

    filtro = {}

    # Búsqueda por nombre
    if search:
        filtro["name"] = {
            "$regex": re.escape(search),
            "$options": "i"
        }

    # Filtro por categoría
    if category:
        categorias_regex = {
            "electrodomesticos": r"^(Electrodomésticos|Electrodomesticos|electrodomesticos)$",
            "computo": r"^(Cómputo|Computo|computo)$",
            "celulares": r"^(Celulares|celulares)$"
        }

        if category in categorias_regex:
            filtro["category"] = {
                "$regex": categorias_regex[category],
                "$options": "i"
            }

    # Filtro por rango de precio
    filtro_precio = {}

    if precio_min:
        try:
            filtro_precio["$gte"] = float(precio_min)
        except ValueError:
            pass

    if precio_max:
        try:
            filtro_precio["$lte"] = float(precio_max)
        except ValueError:
            pass

    if filtro_precio:
        filtro["price"] = filtro_precio

    productos = list(mongo.db.products.find(filtro))

    return render_template(
        "products_list.html",
        productos=productos,
        categoria_actual=category if category else "todos",
        search=search,
    )