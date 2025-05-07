1. Aplicación a probar
La aplicación es una tienda de libros en línea ("BookHaven" o "Libros912") con las siguientes características:

Desarrollada en Python con Flask
Interfaz web (HTML/CSS con Tailwind)
Gestiona un catálogo de libros con CRUD completo
Almacenamiento en archivos JSON
Funcionalidades principales:
Visualizar libros (home, detalle, filtrar por categoría)
Panel de administración (CRUD de libros)
Gestión de imágenes de portada


2. Objetivo y alcance de las pruebas
Objetivo
Verificar la correcta funcionalidad de la aplicación de tienda de libros, asegurando que todas las operaciones CRUD sobre productos funcionen correctamente, así como la gestión de imágenes y la correcta visualización de los diferentes tipos de libros según categorías.

Alcance
Pruebas unitarias: Funciones críticas en books.py y app.py
Pruebas de integración: Flujo completo de CRUD a través de la API
Pruebas de aceptación: Funcionalidad desde la interfaz de usuario
Cobertura mínima: 85% de cobertura de código
3. Especificación de las pruebas
Template de Especificación de Pruebas

| ID | Tipo de prueba | Módulo | Función/Característica | Descripción | Precondiciones | Datos de entrada | Pasos | Resultado esperado | Criticidad |
|----|----------------|--------|------------------------|-------------|----------------|-----------------|-------|-------------------|------------|
| TU-01 | Unitaria | books.py | load_products | Verifica la carga correcta de productos desde el archivo JSON | Archivo JSON válido | N/A | 1. Crear JSON de prueba<br>2. Llamar a load_products | Se cargan correctamente los productos | Alta |


Plan de Pruebas (Ejemplo tabular)

| ID | Tipo | Descripción | Precondiciones | Datos | Pasos | Resultado Esperado | Criticidad |
|----|------|-------------|----------------|-------|-------|-------------------|------------|
| TU-01 | Unitaria | Carga de productos | Archivo JSON válido | N/A | 1. Llamar a load_products() | Productos cargados correctamente | Alta |
| TU-02 | Unitaria | Agregar nuevo producto | N/A | Datos libro válido | 1. Llamar a agregar_producto() | Producto agregado y ID generado | Alta |
| TU-03 | Unitaria | Eliminar producto | Producto existente | ID válido | 1. Llamar a eliminar_producto() | Producto eliminado | Media |
| TU-04 | Unitaria | Actualizar producto | Producto existente | Datos actualizados | 1. Llamar a actualizar_producto() | Producto actualizado | Media |
| TI-01 | Integración | Flujo admin->add->view | N/A | Datos libro | 1. Abrir admin<br>2. Agregar libro<br>3. Ver libro | Libro agregado y visible | Alta |
| TA-01 | Aceptación | Agregar libro | N/A | Datos libro | 1. Ir a Admin<br>2. Llenar formulario<br>3. Submit | Libro agregado correctamente | Alta |


Plan de Pruebas (Ejemplo tabular)
# Test para la función get_next_id()
def test_get_next_id():
    """Prueba que la función get_next_id genere IDs secuenciales correctamente"""
    # Respaldo del archivo original
    if os.path.exists(ID_FILE):
        with open(ID_FILE, 'r') as f:
            backup = f.read()
    
    # Crear un ID file con valor conocido
    with open(ID_FILE, 'w') as f:
        json.dump({'last_id': 42}, f)
    
    # Verificar que el siguiente ID es correcto
    next_id = get_next_id()
    assert next_id == "BK0043"
    
    # Verificar que el archivo se actualizó correctamente
    with open(ID_FILE, 'r') as f:
        data = json.load(f)
        assert data['last_id'] == 43
    
    # Restaurar el archivo original
    if 'backup' in locals():
        with open(ID_FILE, 'w') as f:
            f.write(backup)

# Test para la función actualizar_producto
def test_actualizar_producto_existente():
    """Prueba que la actualización de un producto existente funcione correctamente"""
    # Crear un producto para la prueba
    codigo = agregar_producto(
        "Test Book", 
        "Test Author", 
        "Test Description", 
        10, 
        19.99, 
        "", 
        "Fiction"
    )
    
    # Actualizar el producto
    resultado = actualizar_producto(
        codigo,
        "Updated Title",
        "Updated Author",
        "Updated Description",
        5,
        9.99,
        "",
        "Non-Fiction"
    )
    
    # Verificar el mensaje de éxito
    assert resultado == "Producto actualizado."
    
    # Verificar que el producto fue actualizado correctamente
    productos = load_products()
    assert codigo in productos
    assert productos[codigo]["titulo"] == "Updated Title"
    assert productos[codigo]["autor"] == "Updated Author"
    assert productos[codigo]["stock"] == 5
    assert productos[codigo]["precio"] == 9.99
    assert productos[codigo]["categoria"] == "Non-Fiction"
    
    # Limpieza
    eliminar_producto(codigo)




5. Ejemplos de pruebas de aceptación
Como se trata de una aplicación web desarrollada con Flask, no se puede utilizar Selenium directamente sino siguiendo el patrón "Page Object" para pruebas de aceptación.
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class TestBookStoreUI:
    @pytest.fixture(scope="class")
    def setup_driver(self):
        # Iniciar el servidor Flask en un thread separado (no mostrado aquí)
        # ...
        
        # Configurar Selenium
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("http://localhost:5000")
        yield driver
        driver.quit()
    
    def test_home_page_loads(self, setup_driver):
        """Verificar que la página de inicio carga correctamente"""
        driver = setup_driver
        assert "BookHaven - Home" in driver.title
        
        # Tomar captura de pantalla
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/home_page_load.png")
    
    def test_add_book(self, setup_driver):
        """Verificar que se puede añadir un nuevo libro"""
        driver = setup_driver
        
        # Ir a la página de administración
        driver.get("http://localhost:5000/admin")
        
        # Llenar el formulario
        driver.find_element(By.ID, "titulo").send_keys("Selenium Test Book")
        driver.find_element(By.ID, "autor").send_keys("Selenium Author")
        driver.find_element(By.ID, "descripcion_completa").send_keys("Book added by Selenium test")
        driver.find_element(By.ID, "stock").send_keys("15")
        driver.find_element(By.ID, "precio").send_keys("29.99")
        
        # Seleccionar categoría
        select = driver.find_element(By.ID, "categoria")
        select.find_element(By.XPATH, "//option[text()='Mystery']").click()
        
        # Tomar captura antes de enviar
        driver.save_screenshot("evidence/add_book_form_filled.png")
        
        # Enviar formulario
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add Book')]").click()
        
        # Verificar que el libro aparece en la tabla
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Selenium Test Book')]")))
        assert element is not None
        
        # Tomar captura después de agregar
        driver.save_screenshot("evidence/book_added_successfully.png")




## Prueba de Aceptación Manual: Agregar un nuevo libro

### Precondiciones:
- Aplicación ejecutándose en localhost:5000
- Navegador web Chrome/Firefox actualizado

### Datos de prueba:
- Título: "Manual Test Book"
- Autor: "Manual Tester"
- Descripción: "Este libro fue agregado mediante una prueba manual"
- Stock: 25
- Precio: $19.99
- Categoría: Fiction
- Imagen: book_cover.jpg (preparada previamente)

### Pasos:
1. Abrir el navegador y navegar a http://localhost:5000/admin
2. Verificar que se muestra el formulario de "Add New Book"
3. Completar el formulario con los datos de prueba
4. Hacer clic en el botón "Add Book"
5. Verificar que el libro aparece en la tabla de inventario
6. Hacer clic en "Home" en la navegación superior
7. Verificar que el libro aparece en la página principal
8. Hacer clic en "View details" del libro agregado
9. Verificar que los detalles del libro son correctos

### Evidencia:
- Screenshot 1: Formulario completo antes de enviar (TA01_01_form_filled.png)
- Screenshot 2: Tabla de inventario mostrando el libro agregado (TA01_02_inventory_table.png)
- Screenshot 3: Página principal mostrando el libro (TA01_03_home_page.png)
- Screenshot 4: Página de detalles del libro (TA01_04_book_details.png)

### Resultado Esperado:
El libro se agrega correctamente y aparece tanto en el inventario como en la página principal,
con todos los detalles correctos en la página de detalle del libro.

### Resultado Real:
[A completar durante la ejecución]

### Severidad en caso de fallo:
Mayor (no hay pérdida de datos pero impide funcionalidad principal)



