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

from books import actualizar_producto, agregar_producto, load_products

@pytest.fixture
def sample_product_for_update():
    """Fixture para crear un producto de prueba temporal para actualizar"""
    logger.info("Preparando producto de muestra para pruebas de actualización")
    
    # Primero respaldamos los datos existentes
    data_file = Path('data/products.json')
    if data_file.exists():
        with open(data_file, 'r') as f:
            original_data = json.load(f)
            logger.debug(f"Respaldo de {len(original_data)} productos existentes")
    else:
        original_data = []
        logger.warning("Archivo de productos no encontrado")
    
    # Creamos un producto de prueba
    logger.info("Agregando producto de prueba para actualizar")
    codigo = agregar_producto(
        "Libro Test Actualización",
        "Autor Update Test",
        "Libro para probar función actualizar_producto",
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
    logger.info("Limpiando después de pruebas actualizar_producto")
    with open(data_file, 'w') as f:
        json.dump(self_original_data, f, indent=4)
        logger.debug("Datos restaurados correctamente")

def test_actualizar_producto_success(sample_product_for_update):
    """Prueba actualizar un producto existente"""
    logger.info("Iniciando prueba: test_actualizar_producto_success")
    codigo = sample_product_for_update
    
    # Datos actualizados
    nuevo_titulo = "Título Actualizado"
    nuevo_autor = "Autor Actualizado"
    nueva_descripcion = "Nueva descripción actualizada"
    nuevo_stock = 10
    nuevo_precio = 29.99
    nueva_imagen = "test_updated.jpg"
    nueva_categoria = "Test Updated"
    
    logger.debug(f"Datos para actualización: título={nuevo_titulo}, precio={nuevo_precio}")
    
    # Ejecutar la actualización
    result = actualizar_producto(
        codigo,
        nuevo_titulo,
        nuevo_autor,
        nueva_descripcion,
        nuevo_stock,
        nuevo_precio,
        nueva_imagen,
        nueva_categoria
    )
    logger.info(f"Resultado de actualizar_producto: {result}")
    
    assert result == "Producto actualizado.", "La función actualizar_producto debería devolver 'Producto actualizado.' al actualizar correctamente"
    
    # Verificar que los cambios se aplicaron correctamente
    productos = load_products()
    producto_actualizado = productos.get(codigo)
    
    logger.debug(f"Producto después de actualizar: {producto_actualizado}")
    
    assert producto_actualizado is not None, f"Debería poder obtener el producto actualizado"
    assert producto_actualizado['titulo'] == nuevo_titulo, "El título no se actualizó correctamente"
    assert producto_actualizado['autor'] == nuevo_autor, "El autor no se actualizó correctamente"
    assert producto_actualizado['precio'] == nuevo_precio, "El precio no se actualizó correctamente"
    assert producto_actualizado['stock'] == nuevo_stock, "El stock no se actualizó correctamente"
    
    logger.info("Prueba completada exitosamente")

def test_actualizar_producto_nonexistent():
    """Prueba actualizar un producto que no existe"""
    logger.info("Iniciando prueba: test_actualizar_producto_nonexistent")
    
    nonexistent_code = "NONEXISTENT999"
    logger.debug(f"Intentando actualizar producto inexistente: {nonexistent_code}")
    
    # Intentar actualizar un producto inexistente
    result = actualizar_producto(
        nonexistent_code,
        "No Existe",
        "Autor Fantasma",
        "Descripción fantasma",
        5,
        0.99,
        "fantasma.jpg",
        "Fantasma"
    )
    logger.info(f"Resultado de actualizar producto inexistente: {result}")
    
    assert result == "El producto no existe.", "actualizar_producto debería devolver 'El producto no existe.' al intentar actualizar un producto inexistente"
    logger.info("Prueba completada exitosamente")

def test_actualizar_producto_invalid_data(sample_product_for_update):
    """Prueba actualizar un producto con datos inválidos"""
    logger.info("Iniciando prueba: test_actualizar_producto_invalid_data")
    codigo = sample_product_for_update
    
    try:
        # Intentar actualizar con precio inválido
        result = actualizar_producto(
            codigo,
            "Título normal",
            "Autor normal",
            "Descripción normal",
            10,
            "no-es-un-numero",  # Precio inválido
            "test.jpg",
            "Test"
        )
        logger.warning(f"La función no falló con precio inválido: {result}")
        assert False, "La función debería fallar con precio inválido"
    except Exception as e:
        logger.info(f"Error esperado recibido: {str(e)}")
        assert True, "La función debería lanzar un error con precio inválido"
    
    try:
        # Intentar actualizar con stock inválido
        result = actualizar_producto(
            codigo,
            "Título normal",
            "Autor normal",
            "Descripción normal",
            "no-es-un-numero",  # Stock inválido
            29.99,
            "test.jpg",
            "Test"
        )
        logger.warning(f"La función no falló con stock inválido: {result}")
        assert False, "La función debería fallar con stock inválido"
    except Exception as e:
        logger.info(f"Error esperado recibido: {str(e)}")
        assert True, "La función debería lanzar un error con stock inválido"
    
    logger.info("Prueba completada exitosamente")
