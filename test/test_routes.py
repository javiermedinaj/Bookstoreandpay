import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python para importaciones
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client

def test_index_and_home(client):
    """Prueba las rutas de inicio y home"""
    response = client.get('/')
    assert response.status_code == 200
    
    response = client.get('/home')
    assert response.status_code == 200

def test_filter_by_category(client):
    """Prueba el filtrado por categoría"""
    response = client.get('/categoria/General')
    assert response.status_code == 200
#probar con categoria que no existe agregar automatizacion despues 
def test_admin(client):
    """Prueba el acceso a la página de administración"""
    response = client.get('/admin')
    assert response.status_code == 200

def test_book_detail_invalid(client):
    """Prueba acceder a un detalle de libro que no existe"""
    response = client.get('/book/codigo_inexistente')
    assert response.status_code == 302  # Redirección