import pytest
import sys
import os
import logging
from pathlib import Path
import io
import shutil

# Configuración de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Añadir el directorio principal al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Pruebas simples para operaciones de archivo
UPLOAD_FOLDER = 'static/imgs'

class MockFileStorage:
    """Clase para simular un objeto FileStorage de Flask"""
    def __init__(self, filename, content=b'test content', content_type='image/jpeg'):
        self.filename = filename
        self.content = content
        self.stream = io.BytesIO(content)
        self.content_type = content_type
        self.mimetype = content_type
    
    def save(self, destination):
        """Simula guardar el archivo en el destino indicado"""
        with open(destination, 'wb') as f:
            f.write(self.content)
        return True

def save_uploaded_file(file, upload_folder):
    """Función que simula el guardado de un archivo subido"""
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)
    
    # Verificar si el archivo tiene un nombre válido
    if file and file.filename:
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        return file.filename
    return ""

def is_allowed_file(filename, allowed_extensions=None):
    """Verifica si el archivo tiene una extensión permitida"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

def test_save_uploaded_file():
    """Prueba guardar un archivo subido"""
    logger.info("Iniciando prueba: test_save_uploaded_file")
    
    # Crear archivo de prueba
    test_image = MockFileStorage(
        filename="test_upload.jpg",
        content=b'test image content',
        content_type='image/jpeg'
    )
    
    # Intentar guardar el archivo
    filename = save_uploaded_file(test_image, UPLOAD_FOLDER)
    
    assert filename == test_image.filename, "El nombre del archivo guardado debería coincidir con el original"
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    assert os.path.exists(file_path), "El archivo debería haberse guardado correctamente"
    
    # Limpiar después de la prueba
    if os.path.exists(file_path):
        os.unlink(file_path)
    
    logger.info("Prueba completada exitosamente")

def test_is_allowed_file():
    """Prueba verificar si un archivo tiene una extensión permitida"""
    logger.info("Iniciando prueba: test_is_allowed_file")
    
    # Extensiones permitidas
    allowed = {'jpg', 'jpeg', 'png', 'gif'}
    
    # Verificar archivos con extensiones permitidas
    assert is_allowed_file("test.jpg", allowed), "Debería permitir archivos .jpg"
    assert is_allowed_file("test.JPG", allowed), "Debería permitir archivos .JPG (mayúsculas)"
    assert is_allowed_file("test.jpeg", allowed), "Debería permitir archivos .jpeg"
    assert is_allowed_file("test.png", allowed), "Debería permitir archivos .png"
    assert is_allowed_file("test.gif", allowed), "Debería permitir archivos .gif"
    
    # Verificar archivos con extensiones no permitidas
    assert not is_allowed_file("test.exe", allowed), "No debería permitir archivos .exe"
    assert not is_allowed_file("test.txt", allowed), "No debería permitir archivos .txt"
    assert not is_allowed_file("test", allowed), "No debería permitir archivos sin extensión"
    
    logger.info("Prueba completada exitosamente")

def test_save_no_file():
    """Prueba intentar guardar cuando no hay archivo"""
    logger.info("Iniciando prueba: test_save_no_file")
    
    # Caso 1: filename vacío
    test_empty = MockFileStorage(filename="")
    filename = save_uploaded_file(test_empty, UPLOAD_FOLDER)
    assert filename == "", "Debería devolver string vacío cuando el nombre del archivo está vacío"
    
    # Caso 2: None como archivo
    filename = save_uploaded_file(None, UPLOAD_FOLDER)
    assert filename == "", "Debería manejar correctamente cuando el archivo es None"
    
    logger.info("Prueba completada exitosamente")
