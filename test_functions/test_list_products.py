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

from books import listar_productos

def test_listar_productos_exists():
    """Prueba que la función listar_productos existe y devuelve datos"""
    logger.info("Iniciando prueba: test_listar_productos_exists")
    
    productos = listar_productos()
    logger.debug(f"Productos listados: {len(productos)}")
    
    assert isinstance(productos, dict), "listar_productos debe devolver un diccionario"
    
    # Si hay productos, verificar estructura
    if productos:
        # Tomar la primera clave
        primera_clave = next(iter(productos))
        primer_producto = productos[primera_clave]
        logger.debug(f"Primer producto: {primera_clave} - {primer_producto}")
        
        # Verificar estructura del producto
        assert 'codigo' in primer_producto, "El producto debe tener código"
        assert 'titulo' in primer_producto, "El producto debe tener título"
        assert 'autor' in primer_producto, "El producto debe tener autor"
    
    logger.info("Prueba completada exitosamente")

@pytest.fixture
def backup_products_data():
    """Fixture para respaldar y restaurar datos de productos"""
    logger.info("Preparando respaldo de productos")
    
    # Respaldamos los datos existentes
    data_file = Path('data/products.json')
    backup_file = Path('data/products.json.bak')
    
    if data_file.exists():
        with open(data_file, 'r') as f:
            logger.debug("Creando respaldo de productos")
            shutil.copy2(data_file, backup_file)
    
    yield
    
    # Restaurar datos originales
    logger.info("Restaurando datos originales")
    if backup_file.exists():
        shutil.copy2(backup_file, data_file)
        backup_file.unlink()  # Eliminar backup
        logger.debug("Datos restaurados correctamente")

def test_listar_productos_estructura():
    """Prueba la estructura de los productos listados"""
    logger.info("Iniciando prueba: test_listar_productos_estructura")
    
    productos = listar_productos()
    logger.info(f"Productos listados: {len(productos)}")
    
    # Verificar la estructura de los productos
    for codigo, producto in productos.items():
        logger.debug(f"Verificando producto: {codigo}")
        assert 'codigo' in producto, "El producto debe tener código"
        assert 'titulo' in producto, "El producto debe tener título"
        assert 'autor' in producto, "El producto debe tener autor"
        assert 'precio' in producto, "El producto debe tener precio"
        assert codigo == producto['codigo'], "El código debe coincidir con la clave"
    
    logger.info("Prueba completada exitosamente")
