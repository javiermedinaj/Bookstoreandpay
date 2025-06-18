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

from books import load_products

@pytest.fixture
def sample_product():
    """Fixture para crear un producto de prueba temporal"""
    logger.info("Preparando producto de muestra para pruebas")
    # Primero respaldamos los datos existentes
    data_file = Path('data/products.json')
    if data_file.exists():
        with open(data_file, 'r') as f:
            original_data = json.load(f)
            logger.debug(f"Respaldo de datos existentes")
    else:
        original_data = {}
        logger.warning("Archivo de productos no encontrado")
    
    # Creamos un producto de prueba con ID conocido
    test_code = "TEST001"
    test_product = {
        "codigo": test_code,
        "titulo": "Libro Test Get",
        "autor": "Autor Get Test",
        "descripcion_completa": "Libro para probar función get_product",
        "stock": 5,
        "precio": 19.99,
        "categoria": "Test",
        "imagen": "test.jpg"
    }
    
    # Añadimos el producto a los datos existentes
    test_products = original_data.copy()
    test_products[test_code] = test_product
    
    with open(data_file, 'w') as f:
        json.dump(test_products, f, indent=4)
        logger.info(f"Producto de prueba agregado: {test_code}")
    
    yield test_code  # Devolvemos el código del producto para usarlo en las pruebas
    
    # Restaurar datos originales
    logger.info("Limpiando después de pruebas get_product")
    with open(data_file, 'w') as f:
        json.dump(original_data, f, indent=4)
        logger.debug("Datos restaurados correctamente")

def get_product(codigo):
    """Función auxiliar para obtener un producto específico"""
    productos = load_products()
    return productos.get(codigo)

def test_get_product_existing(sample_product):
    """Prueba obtener un producto existente por su código"""
    logger.info(f"Iniciando prueba: test_get_product_existing")
    code = sample_product
    logger.debug(f"Buscando producto con código: {code}")
    
    product = get_product(code)
    logger.info(f"Producto obtenido: {product}")
    
    assert product is not None, f"Debería encontrar el producto con código {code}"
    assert product['codigo'] == code, f"El código del producto debería ser {code}"
    assert product['titulo'] == "Libro Test Get", "El título no coincide"
    logger.info("Prueba completada exitosamente")

def test_get_product_nonexistent():
    """Prueba obtener un producto que no existe"""
    logger.info("Iniciando prueba: test_get_product_nonexistent")
    code = "NONEXISTENT999"
    logger.debug(f"Buscando producto inexistente con código: {code}")
    
    product = get_product(code)
    logger.info(f"Resultado de búsqueda de producto inexistente: {product}")
    
    assert product is None, f"No debería encontrar ningún producto con código {code}"
    logger.info("Prueba completada exitosamente")

def test_get_all_products():
    """Prueba que load_products devuelva un diccionario de productos"""
    logger.info("Iniciando prueba: test_get_all_products")
    
    productos = load_products()
    logger.info(f"Obtenidos {len(productos)} productos")
    
    assert isinstance(productos, dict), "load_products debería devolver un diccionario"
    
    # Verificar la estructura de al menos un producto si hay alguno
    if productos:
        first_code = next(iter(productos))
        first_product = productos[first_code]
        logger.debug(f"Primer producto: {first_code} - {first_product}")
        
        assert 'codigo' in first_product, "Los productos deberían tener el campo 'codigo'"
        assert 'titulo' in first_product, "Los productos deberían tener el campo 'titulo'"
        assert 'precio' in first_product, "Los productos deberían tener el campo 'precio'"
    
    logger.info("Prueba completada exitosamente")

def test_get_products_empty():
    """Prueba load_products con un archivo vacío o inexistente"""
    logger.info("Iniciando prueba: test_get_products_empty")
    
    # Respaldamos el archivo actual
    data_file = Path('data/products.json')
    backup_file = Path('data/products_backup.json')
    
    if data_file.exists():
        logger.debug("Respaldando archivo de productos")
        with open(data_file, 'r') as f:
            original_data = f.read()
        with open(backup_file, 'w') as f:
            f.write(original_data)
    
    try:
        # Creamos un archivo vacío
        logger.debug("Creando archivo de productos vacío para prueba")
        with open(data_file, 'w') as f:
            f.write('{}')
        
        # Probamos la función
        productos = load_products()
        logger.info(f"Resultado con archivo vacío: {productos}")
        assert isinstance(productos, dict), "Debería devolver un diccionario"
        assert len(productos) == 0, "El diccionario debería estar vacío"
        
    finally:
        # Restauramos el archivo original
        if backup_file.exists():
            logger.debug("Restaurando archivo de productos original")
            with open(backup_file, 'r') as f:
                original_data = f.read()
            with open(data_file, 'w') as f:
                f.write(original_data)
            backup_file.unlink()  # Eliminamos el respaldo
    
    logger.info("Prueba completada exitosamente")
