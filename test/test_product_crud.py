import os
import io
import sys
import logging
from pathlib import Path

# Agregar el directorio raíz al path de Python para importaciones
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import pytest
from app import app
from books import load_products, DATA_FILE

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    # Backup current data file contents if exist
    backup = None
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            backup = f.read()
    
    logger.info("Iniciando cliente de prueba con modo TESTING activado")
    with app.test_client() as test_client:
        yield test_client

    # Teardown: restore data file after tests
    logger.info("Restaurando datos originales después de las pruebas")
    if backup is not None:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            f.write(backup)
    elif os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

@pytest.fixture
def added_product(client):
    """Fixture que agrega un producto y devuelve su código"""
    print("FIXTURE: Preparando producto de prueba para usar en múltiples tests")
    data = {
        'titulo': 'Test Book',
        'autor': 'Author Test',
        'descripcion_completa': 'A test description',
        'stock': '10',
        'precio': '15.99',
        'categoria': 'General',
        'image': (io.BytesIO(b"dummy image data"), "test.jpg")
    }
    
    print(f"FIXTURE: Agregando libro '{data['titulo']}' por '{data['autor']}'")
    client.post('/add_product', data=data, content_type='multipart/form-data')
    
    # Encontrar el código del producto agregado
    products = load_products()
    for code, product in products.items():
        if product['titulo'] == 'Test Book':
            print(f"FIXTURE: Producto agregado con código {code}")
            return code
    
    print("FIXTURE: ¡ADVERTENCIA! No se pudo agregar el producto de prueba")
    return None

def test_add_product(client):
    """Prueba la adición de un nuevo producto"""
    print("\n------------------------------------------------------")
    print("TEST 1: Prueba de agregar un nuevo producto al catálogo")
    print("------------------------------------------------------")
    
    data = {
        'titulo': 'Test Book',
        'autor': 'Author Test',
        'descripcion_completa': 'A test description',
        'stock': '10',
        'precio': '15.99',
        'categoria': 'General'
    }
    # Simulate a dummy image file
    dummy_image = (io.BytesIO(b"dummy image data"), "test.jpg")
    data['image'] = dummy_image

    print(f"Enviando datos del libro: '{data['titulo']}' por '{data['autor']}'")
    print(f"Precio: ${data['precio']}, Stock: {data['stock']}, Categoría: {data['categoria']}")
    
    response = client.post('/add_product', data=data, content_type='multipart/form-data', follow_redirects=False)
    print(f"Respuesta del servidor: código {response.status_code} (302=Redirected)")
    assert response.status_code == 302, "La adición de producto debería redirigir"

    # Verify that one product exists
    products = load_products()
    print(f"Productos en el sistema después de agregar: {len(products)}")
    assert len(products) > 0, "Debería haber al menos un producto"
    
    # Find our test product
    codigo = None
    for code, product in products.items():
        if product['titulo'] == 'Test Book':
            codigo = code
            break
    
    assert codigo is not None, "Product wasn't added successfully"
    print(f"Producto agregado correctamente con código: {codigo}")
    print("TEST 1: COMPLETADO CON ÉXITO")

def test_edit_product_page(client, added_product):
    """Prueba que se muestre correctamente el formulario de edición"""
    print("\n------------------------------------------------------")
    print("TEST 2: Prueba de visualización del formulario de edición")
    print("------------------------------------------------------")
    print(f"Accediendo al formulario de edición para el libro con código: {added_product}")
    
    # Verificar que se muestra el formulario de edición
    response = client.get(f'/edit_product/{added_product}')
    print(f"Respuesta del servidor: código {response.status_code} (200=OK)")
    assert response.status_code == 200, "Debería mostrar el formulario de edición"
    print("TEST 2: COMPLETADO CON ÉXITO")

def test_update_product(client, added_product):
    """Prueba la actualización de un producto existente"""
    print("\n------------------------------------------------------")
    print("TEST 3: Prueba de actualización de un producto existente")
    print("------------------------------------------------------")
    print(f"Actualizando el libro con código: {added_product}")
    
    # Actualizar producto
    updated_data = {
        'titulo': 'Updated Test Book',
        'autor': 'Updated Author',
        'descripcion_completa': 'An updated description',
        'stock': '5',
        'precio': '9.99',
        'categoria': 'General'
    }
    dummy_empty = (io.BytesIO(b''), '')
    updated_data['image'] = dummy_empty

    print(f"Enviando datos actualizados: '{updated_data['titulo']}' por '{updated_data['autor']}'")
    print(f"Nuevo precio: ${updated_data['precio']}, Nuevo stock: {updated_data['stock']}")
    
    response = client.post(f'/update_product/{added_product}', data=updated_data, content_type='multipart/form-data', follow_redirects=False)
    print(f"Respuesta del servidor: código {response.status_code} (302=Redirected)")
    assert response.status_code == 302, "La actualización debería redirigir"

    # Verify update in storage
    products = load_products()
    assert added_product in products, f"El producto con código {added_product} ya no existe"
    updated_product = products.get(added_product)
    print(f"Verificando datos actualizados del producto {added_product}:")
    print(f"Título: '{updated_product['titulo']}' (esperado: 'Updated Test Book')")
    print(f"Stock: {updated_product['stock']} (esperado: 5)")
    
    assert updated_product['titulo'] == 'Updated Test Book', "El título no se actualizó correctamente"
    assert updated_product['stock'] == 5, "El stock no se actualizó correctamente"
    
    print("TEST 3: COMPLETADO CON ÉXITO")

def test_book_detail(client, added_product):
    """Prueba la página de detalles de un libro"""
    print("\n------------------------------------------------------")
    print("TEST 4: Prueba de visualización de detalles de un libro")
    print("------------------------------------------------------")
    print(f"Accediendo a los detalles del libro con código: {added_product}")
    
    # Verificar página de detalles
    response = client.get(f'/book/{added_product}')
    print(f"Respuesta del servidor: código {response.status_code} (200=OK)")
    assert response.status_code == 200, "Debería mostrar los detalles del libro"
    print("TEST 4: COMPLETADO CON ÉXITO")

def test_delete_product(client, added_product):
    """Prueba la eliminación de un producto"""
    print("\n------------------------------------------------------")
    print("TEST 5: Prueba de eliminación de un producto")
    print("------------------------------------------------------")
    
    # Actualizar para tener un título único para verificar eliminación
    updated_data = {
        'titulo': 'Book To Delete',
        'autor': 'Author',
        'descripcion_completa': 'Description',
        'stock': '5',
        'precio': '9.99',
        'categoria': 'General',
        'image': (io.BytesIO(b''), '')
    }
    print(f"Preparando libro para eliminación: cambiando título a '{updated_data['titulo']}'")
    client.post(f'/update_product/{added_product}', data=updated_data, content_type='multipart/form-data')
    
    print(f"Solicitando eliminación del libro con código: {added_product}")
    # Eliminar producto
    response = client.get(f'/delete_product/{added_product}', follow_redirects=False)
    print(f"Respuesta del servidor: código {response.status_code} (302=Redirected)")
    assert response.status_code == 302, "La eliminación debería redirigir"
    
    # Verificar eliminación
    products = load_products()
    print(f"Verificando que '{updated_data['titulo']}' ya no existe en el catálogo")
    found = False
    for code, product in products.items():
        if product['titulo'] == 'Book To Delete':
            found = True
            break
    
    assert not found, "El producto no fue eliminado correctamente"
    print("Producto eliminado exitosamente")
    print("TEST 5: COMPLETADO CON ÉXITO")