8. Clasificación de defectos
Criterios de clasificación:
Categoría	Descripción	Ejemplo
Bloqueante	Impide continuar con las pruebas o el uso de la aplicación	La aplicación no inicia, error 500 en todas las rutas
Crítico	Causa pérdida de datos o fallo grave en funcionalidad principal	Los libros se guardan con datos corruptos o se pierden al actualizar
Mayor	Afecta significativamente la funcionalidad pero hay alternativas	Filtrado por categoría no funciona pero se pueden ver todos los libros
Menor	Problemas menores que no afectan la funcionalidad principal	Formato de precio incorrecto pero el valor es correcto
Trivial	Problemas estéticos o de mejora	Desalineación de elementos, títulos cortados en la interfaz


## Defecto: DEF-001

### Título: 
El filtro de categorías no muestra productos tras seleccionar "Mystery"

### Severidad: 
Mayor

### Ambiente:
- SO: Linux Fedora 41
- Navegador: Chrome 125.0.6422.112
- Resolución: 1920x1080

### Pasos para reproducir:
1. Navegar a la página principal
2. Hacer clic en "Categories" en la barra superior
3. Seleccionar "Mystery" del menú desplegable

### Comportamiento esperado:
Se muestran solo los libros de la categoría "Mystery"

### Comportamiento real:
La página carga pero no muestra ningún libro, aparece mensaje "No books found in this category" aunque existen libros en esa categoría

### Evidencia:
- Screenshot: DEF001_category_filter_empty.png
- Console log: DEF001_console.txt

### Notas adicionales:
El problema no ocurre con otras categorías como "Fiction" o "General"