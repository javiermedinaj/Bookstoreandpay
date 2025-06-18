import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'products.json')
ID_FILE = os.path.join(DATA_DIR, 'lastid.json')

os.makedirs(DATA_DIR, exist_ok=True)

productos = {}

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

    os.makedirs(os.path.dirname(ID_FILE), exist_ok=True)
    
    with open(ID_FILE, 'w') as file:
        json.dump({'last_id': next_id}, file)

    return next_id

def save_products():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(productos, file, ensure_ascii=False, indent=4)

def load_products():
    global productos
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                productos = json.load(file)
                # Comment out or remove the type conversion code
                # for codigo, producto in productos.items():
                #     if 'stock' in producto:
                #         try:
                #             producto['stock'] = int(producto['stock']) if isinstance(producto['stock'], str) else producto['stock']
                #         except ValueError:
                #             logger.warning(f"Invalid stock value for product {codigo}: {producto.get('stock')}. Setting to 0.")
                #             producto['stock'] = 0
                    
                #     if 'precio' in producto:
                #         try:
                #             producto['precio'] = float(producto['precio']) if isinstance(producto['precio'], str) else producto['precio']
                #         except ValueError:
                #             logger.warning(f"Invalid price value for product {codigo}: {producto.get('precio')}. Setting to 0.0.")
                #             producto['precio'] = 0.0
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error loading products file: {e}")
            productos = {}
    else:
        logger.info(f"Products file not found at {DATA_FILE}")
        productos = {}
    return productos

def agregar_producto(titulo, autor, descripcion_completa, stock, precio, imagen, categoria="General"):
    global productos
    load_products()
    # try:
    #     stock = int(stock)
    # except (ValueError, TypeError):
    #     stock = 0
        
    # try:
    #     precio = float(precio)
    # except (ValueError, TypeError):
    #     precio = 0
    
    codigo = get_next_id()
    codigo_formateado = f"BK{codigo:04d}"
    
    productos[codigo_formateado] = {
        "codigo": codigo_formateado,
        "titulo": titulo,
        "autor": autor,
        "descripcion_completa": descripcion_completa,
        "stock": stock,
        "precio": precio,
        "imagen": imagen,
        "categoria": categoria
    }
    
    save_products()
    return codigo_formateado

def eliminar_producto(codigo):
    global productos
    load_products()
    
    if codigo in productos:
        del productos[codigo]
        save_products()
        return f"Producto {codigo} eliminado con éxito."
    else:
        return "El producto no existe."

def actualizar_producto(codigo, titulo, autor, descripcion_completa, stock, precio, imagen, categoria="General"):
    global productos
    load_products()

    # try:
    #     stock = int(stock)
    # except (ValueError, TypeError):
    #     stock = 0
        
    # try:
    #     precio = float(precio)
    # except (ValueError, TypeError):
    #     precio = 0

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