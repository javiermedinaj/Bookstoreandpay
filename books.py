import json
import os

DATA_FILE = 'data/products.json'
ID_FILE = 'data/lastid.json'
IMAGE_FOLDER = 'static/imgs'

productos = {}

def load_products():
    global productos
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                productos = json.load(file)
                for codigo, producto in productos.items():
                    if 'categoria' not in producto:
                        producto['categoria'] = 'General'
                    if 'autor' not in producto:
                        producto['autor'] = ''
                    if 'descripcion_completa' not in producto:
                        producto['descripcion_completa'] = ''
        except json.JSONDecodeError:
            productos = {}
    return productos

def save_products():
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(productos, file, indent=4)

def get_next_id():
    if os.path.exists(ID_FILE):
        try:
            with open(ID_FILE, 'r') as file:
                data = json.load(file)
                last_id = data.get('last_id', 0)
        except (json.JSONDecodeError, FileNotFoundError):
            last_id = 0
    else:
        last_id = 0
    
    next_id = last_id + 1
    
    with open(ID_FILE, 'w') as file:
        json.dump({'last_id': next_id}, file)
    
    return f"BK{next_id:04d}"

def agregar_producto(titulo, autor, descripcion_completa, stock, precio, imagen, categoria="General"):
    global productos
    load_products()
    
    codigo = get_next_id()

    producto = {
        "codigo": codigo,
        "titulo": titulo,
        "autor": autor,
        "descripcion_completa": descripcion_completa,
        "stock": stock,
        "precio": precio,
        "imagen": imagen,
        "categoria": categoria
    }
    productos[codigo] = producto
    save_products()
    return codigo

def eliminar_producto(codigo):
    global productos
    load_products()
    if codigo in productos:
        del productos[codigo]
        save_products()
        return "Producto eliminado."
    else:
        return "El producto no existe."

def actualizar_producto(codigo, titulo, autor, descripcion_completa, stock, precio, imagen, categoria="General"):
    global productos
    load_products()

    if codigo in productos:
        productos[codigo] = {
            "codigo": codigo,
            "titulo": titulo,
            "autor": autor,
            "descripcion_completa": descripcion_completa,
            "stock": stock,
            "precio": precio,
            "imagen": imagen,
            "categoria": categoria
        }
        save_products()
        return "Producto actualizado."
    else:
        return "El producto no existe."

def listar_productos():
    global productos
    load_products()
    return productos

load_products()