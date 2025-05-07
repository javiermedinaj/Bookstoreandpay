import os
import io
import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python para importaciones
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import pytest
from app import app
from books import load_products, DATA_FILE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    # Backup current data file contents if exist
    backup = None
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            backup = f.read()
    
    with app.test_client() as test_client:
        yield test_client

    # Teardown: restore data file after tests
    if backup is not None:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            f.write(backup)
    elif os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

@pytest.fixture
def added_product(client):
    """Fixture que agrega un producto y devuelve su código"""
    data = {
        'titulo': 'Test Book',
        'autor': 'Author Test',
        'descripcion_completa': 'A test description',
        'stock': '10',
        'precio': '15.99',
        'categoria': 'General',
        'image': (io.BytesIO(b"dummy image data"), "test.jpg")
    }
    
    client.post('/add_product', data=data, content_type='multipart/form-data')
    
    # Encontrar el código del producto agregado
    products = load_products()
    for code, product in products.items():
        if product['titulo'] == 'Test Book':
            return code
    
    return None