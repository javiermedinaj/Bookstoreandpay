import pytest
import sys
import os
import json
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Añadir el directorio principal al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from books import load_products, save_products

@pytest.fixture
def sample_categorized_products():
    """Fixture para crear productos de prueba con diferentes categorías"""
    logger.info("Preparando productos por categorías para pruebas")
    
    # Respaldamos los datos existentes
    data_file = Path('data/products.json')
    if data_file.exists():
        with open(data_file, 'r') as f:
            original_data = json.load(f)
            logger.debug(f"Respaldo de datos originales")
    else:
        original_data = {}
        logger.warning("Archivo de productos no encontrado")
    
    # Creamos productos de prueba con diferentes categorías
    test_products = {
        "BK0001": {
            "codigo": "BK0001",
            "titulo": "Libro Ficción 1",
            "autor": "Autor Ficción",
            "descripcion_completa": "Libro de ficción para pruebas",
            "stock": 10,
            "precio": 19.99,
            "categoria": "Fiction",
            "imagen": "test.jpg"
        },
        "BK0002": {
            "codigo": "BK0002",
            "titulo": "Libro Ficción 2",
            "autor": "Autor Ficción",
            "descripcion_completa": "Otro libro de ficción para pruebas",
            "stock": 5,
            "precio": 29.99,
            "categoria": "Fiction",
            "imagen": "test.jpg"
        },
        "BK0003": {
            "codigo": "BK0003",
            "titulo": "Libro Ciencia 1",
            "autor": "Autor Ciencia",
            "descripcion_completa": "Libro de ciencia para pruebas",
            "stock": 8,
            "precio": 24.99,
            "categoria": "Science",
            "imagen": "test.jpg"
        },
        "BK0004": {
            "codigo": "BK0004",
            "titulo": "Libro Misterio 1",
            "autor": "Autor Misterio",
            "descripcion_completa": "Libro de misterio para pruebas",
            "stock": 15,
            "precio": 15.99,
            "categoria": "Mystery",
            "imagen": "test.jpg"
        }
    }
    
    # Guardamos los productos de prueba (no usamos save_products porque queremos un control directo)
    with open(data_file, 'w') as f:
        json.dump(test_products, f, indent=4)
        logger.info("Productos de prueba creados")
    
    categories_count = {
        "Fiction": 2,
        "Science": 1,
        "Mystery": 1
    }
    
    yield categories_count  # Devolvemos el conteo por categoría
    
    # Restauramos los datos originales
    logger.info("Restaurando datos originales")
    with open(data_file, 'w') as f:
        json.dump(original_data, f, indent=4)
        logger.debug("Datos restaurados correctamente")

def filtrar_productos_por_categoria(categoria):
    """Función de filtrado similar a la de app.py pero sin la parte del template"""
    productos = load_products()
    productos_filtrados = {
        codigo: producto for codigo, producto in productos.items()
        if producto.get('categoria') == categoria
    }
    return productos_filtrados

def test_filtrar_por_categoria_fiction(sample_categorized_products):
    """Prueba filtrar productos por categoría Fiction"""
    logger.info("Iniciando prueba: test_filtrar_por_categoria_fiction")
    
    category = "Fiction"
    logger.debug(f"Filtrando por categoría: {category}")
    
    # Llamamos a la función de filtrado
    productos_filtrados = filtrar_productos_por_categoria(category)
    logger.debug("Filtrado completado")
    
    expected_count = sample_categorized_products[category]
    logger.debug(f"Cantidad esperada: {expected_count}")
    
    assert len(productos_filtrados) == expected_count, f"Deberían haber {expected_count} productos en la categoría {category}"
    
    # Verificar que todos los productos son de la categoría correcta
    for codigo, producto in productos_filtrados.items():
        logger.debug(f"Verificando producto: {codigo}")
        assert producto['categoria'] == category, f"El producto {codigo} no pertenece a la categoría {category}"
    
    logger.info("Prueba completada exitosamente")

def test_filtrar_por_categoria_science(sample_categorized_products):
    """Prueba filtrar productos por categoría Science"""
    logger.info("Iniciando prueba: test_filtrar_por_categoria_science")
    
    category = "Science"
    logger.debug(f"Filtrando por categoría: {category}")
    
    # Llamamos a la función de filtrado
    productos_filtrados = filtrar_productos_por_categoria(category)
    logger.debug("Filtrado completado")
    
    expected_count = sample_categorized_products[category]
    logger.debug(f"Cantidad esperada: {expected_count}")
    
    assert len(productos_filtrados) == expected_count, f"Deberían haber {expected_count} productos en la categoría {category}"
    
    # Verificar que todos los productos son de la categoría correcta
    for codigo, producto in productos_filtrados.items():
        logger.debug(f"Verificando producto: {codigo}")
        assert producto['categoria'] == category, f"El producto {codigo} no pertenece a la categoría {category}"
    
    logger.info("Prueba completada exitosamente")

def test_filtrar_por_categoria_nonexistent():
    """Prueba filtrar por una categoría que no existe"""
    logger.info("Iniciando prueba: test_filtrar_por_categoria_nonexistent")
    
    category = "NonexistentCategory"
    logger.debug(f"Filtrando por categoría inexistente: {category}")
    
    # Llamamos a la función de filtrado
    productos_filtrados = filtrar_productos_por_categoria(category)
    logger.debug("Filtrado completado")
    
    assert len(productos_filtrados) == 0, f"No deberían haber productos en la categoría inexistente {category}"
    
    logger.info("Prueba completada exitosamente")
