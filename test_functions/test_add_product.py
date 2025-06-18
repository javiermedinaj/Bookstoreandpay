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

from books import agregar_producto, load_products, save_products

@pytest.fixture
def test_data():
    """Fixture para proporcionar datos de prueba"""
    logger.info("Preparando datos de prueba para agregar_producto")
    return {
        "titulo": "Libro de Prueba",
        "autor": "Autor Test",
        "descripcion_completa": "Descripción de prueba",
        "stock": 10,
        "precio": 29.99,
        "categoria": "Fiction",
        "imagen": "test.jpg"
    }

@pytest.fixture
def cleanup_test_data():
    """Fixture para limpiar después de las pruebas"""
    logger.info("Iniciando limpieza para prueba de agregar_producto")
    # Código que se ejecuta antes de la prueba
    data_file = Path('data/products.json')
    if data_file.exists():
        with open(data_file, 'r') as f:
            original_data = json.load(f)
            logger.debug(f"Respaldo de datos originales")
    else:
        original_data = {}
        logger.warning("Archivo de productos no encontrado, se creará uno nuevo")
    
    yield  # Aquí se ejecuta la prueba
    
    # Código que se ejecuta después de la prueba (limpieza)
    logger.info("Restaurando datos originales después de la prueba")
    with open(data_file, 'w') as f:
        json.dump(original_data, f, indent=4)
        logger.debug("Datos restaurados correctamente")

def test_agregar_producto_success(test_data, cleanup_test_data):
    """Prueba que un producto se añada correctamente"""
    logger.info("Iniciando prueba: test_agregar_producto_success")
    logger.debug(f"Datos de prueba: {test_data}")
    
    # Obtener productos iniciales
    productos_antes = load_products()
    count_antes = len(productos_antes)
    logger.debug(f"Cantidad de productos antes: {count_antes}")
    
    # Ejecutar la función
    result = agregar_producto(
        test_data["titulo"],
        test_data["autor"],
        test_data["descripcion_completa"],
        test_data["stock"],
        test_data["precio"],
        test_data["imagen"],
        test_data["categoria"]
    )
    
    logger.info(f"Resultado de agregar_producto: {result}")
    assert result is not None, "La función agregar_producto debería devolver un código"
    
    # Verificar que el producto se añadió al archivo JSON
    productos_despues = load_products()
    count_despues = len(productos_despues)
    logger.debug(f"Cantidad de productos después: {count_despues}")
    
    assert count_despues == count_antes + 1, "Debería haberse añadido un producto"
    
    # Buscar el producto añadido por su código
    found = False
    for codigo, producto in productos_despues.items():
        if codigo == result:
            found = True
            logger.debug(f"Producto encontrado: {producto}")
            assert producto["titulo"] == test_data["titulo"], "El título no coincide"
            assert producto["autor"] == test_data["autor"], "El autor no coincide"
            break
    
    assert found, "El producto no se encontró en el archivo JSON"
    logger.info("Prueba completada exitosamente")

def test_agregar_producto_valores_invalidos():
    """Prueba que falle al añadir un producto con valores inválidos"""
    logger.info("Iniciando prueba: test_agregar_producto_valores_invalidos")
    
    # Intentar agregar con precio inválido (string)
    try:
        result = agregar_producto(
            "Libro Inválido",
            "Autor Test",
            "Descripción de prueba",
            10,
            "no-es-un-numero",  # Precio inválido
            "test.jpg",
            "Fiction"
        )
        logger.warning(f"La función no falló con precio inválido: {result}")
        assert False, "La función debería fallar con precio inválido"
    except Exception as e:
        logger.info(f"Error esperado recibido: {str(e)}")
        assert True, "La función debería lanzar un error con precio inválido"
    
    # Intentar agregar con stock inválido
    try:
        result = agregar_producto(
            "Libro Inválido",
            "Autor Test",
            "Descripción de prueba",
            "no-es-un-numero",  # Stock inválido
            29.99,
            "test.jpg",
            "Fiction"
        )
        logger.warning(f"La función no falló con stock inválido: {result}")
        assert False, "La función debería fallar con stock inválido"
    except Exception as e:
        logger.info(f"Error esperado recibido: {str(e)}")
        assert True, "La función debería lanzar un error con stock inválido"
    
    logger.info("Prueba completada exitosamente")
