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

from books import eliminar_producto, agregar_producto, load_products

@pytest.fixture
def sample_product_for_delete():
    """Fixture para crear un producto de prueba temporal para eliminar"""
    logger.info("Preparando producto de muestra para pruebas de eliminación")
    
    # Primero respaldamos los datos existentes
    data_file = Path('data/products.json')
    if data_file.exists():
        with open(data_file, 'r') as f:
            original_data = json.load(f)
            logger.debug(f"Respaldo de datos originales")
    else:
        original_data = {}
        logger.warning("Archivo de productos no encontrado")
    
    # Creamos un producto de prueba
    logger.info("Agregando producto de prueba para eliminar")
    codigo = agregar_producto(
        "Libro Test Eliminación",
        "Autor Delete Test",
        "Libro para probar función eliminar_producto",
        5,
        19.99,
        "test.jpg",
        "Test"
    )
    
    logger.info(f"Producto de prueba agregado con código: {codigo}")
    
    # Guardamos copia de los datos originales para restaurar después
    self_original_data = original_data.copy()
    
    yield codigo  # Devolvemos el código para usarlo en las pruebas
    
    # Restaurar datos originales
    logger.info("Limpiando después de pruebas eliminar_producto")
    with open(data_file, 'w') as f:
        json.dump(self_original_data, f, indent=4)
        logger.debug("Datos restaurados correctamente")

def test_eliminar_producto_success(sample_product_for_delete):
    """Prueba eliminar un producto existente"""
    logger.info("Iniciando prueba: test_eliminar_producto_success")
    
    codigo = sample_product_for_delete
    logger.debug(f"Intentando eliminar producto con código: {codigo}")
    
    # Contar productos antes de eliminar
    productos_antes = load_products()
    count_antes = len(productos_antes)
    logger.debug(f"Cantidad de productos antes de eliminar: {count_antes}")
    
    # Ejecutar eliminación
    result = eliminar_producto(codigo)
    logger.info(f"Resultado de eliminar_producto: {result}")
    
    assert result == "Producto eliminado.", "La función eliminar_producto debería devolver 'Producto eliminado.' al eliminar correctamente"
    
    # Verificar que el producto ya no existe
    productos_despues = load_products()
    count_despues = len(productos_despues)
    logger.debug(f"Cantidad de productos después de eliminar: {count_despues}")
    
    assert count_despues == count_antes - 1, "La cantidad total de productos debería haber disminuido en 1"
    
    # Verificar que el producto realmente fue eliminado
    assert codigo not in productos_despues, f"El producto con código {codigo} no debería existir después de eliminarlo"
    
    logger.info("Prueba completada exitosamente")

def test_eliminar_producto_nonexistent():
    """Prueba eliminar un producto que no existe"""
    logger.info("Iniciando prueba: test_eliminar_producto_nonexistent")
    
    nonexistent_code = "NONEXISTENT999"
    logger.debug(f"Intentando eliminar producto inexistente: {nonexistent_code}")
    
    # Contar productos antes de intentar eliminar
    productos_antes = load_products()
    count_antes = len(productos_antes)
    logger.debug(f"Cantidad de productos antes: {count_antes}")
    
    # Intentar eliminar producto inexistente
    result = eliminar_producto(nonexistent_code)
    logger.info(f"Resultado de eliminar producto inexistente: {result}")
    
    assert result == "El producto no existe.", "eliminar_producto debería devolver 'El producto no existe.' al intentar eliminar un producto inexistente"
    
    # Verificar que la cantidad de productos no cambió
    productos_despues = load_products()
    count_despues = len(productos_despues)
    logger.debug(f"Cantidad de productos después: {count_despues}")
    
    assert count_despues == count_antes, "La cantidad de productos no debería cambiar"
    
    logger.info("Prueba completada exitosamente")
