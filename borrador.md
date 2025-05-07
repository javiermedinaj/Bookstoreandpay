1. OBJETIVO
   Verificar la funcionalidad completa de la aplicación de tienda de libros,
   asegurando que todas las operaciones CRUD sobre el catálogo de libros 
   funcionan correctamente, validando tanto la lógica interna como la 
   experiencia de usuario desde la interfaz web.

2. ALCANCE
   Este plan de pruebas abarca:
   • Pruebas unitarias sobre las funciones core en books.py y app.py
   • Pruebas de integración para los flujos CRUD completos
   • Pruebas de aceptación desde la interfaz de usuario
   • Verificación de manejo de errores y casos límite
   • Se excluye del alcance: pruebas de rendimiento, seguridad y escalabilidad

3. DESARROLLO
   3.1. Descripción de la aplicación a probar
      BookHaven es una aplicación web desarrollada con Flask (Python) que 
      permite gestionar un catálogo de libros. La aplicación ofrece:
      
      • Visualización de libros con filtrado por categoría
      • Página de detalle para cada libro
      • Panel de administración para gestión CRUD
      • Carga de imágenes de portada
      • Almacenamiento persistente en archivos JSON
      
      La arquitectura es simple: Flask maneja el ruteo y las vistas, mientras
      que el módulo books.py implementa la lógica de negocio y persistencia.
      
      [Insertar diagrama de arquitectura]
   
   3.2. Objetivo y alcance de las pruebas
      [Expandir contenido de las secciones 1 y 2]
   
   3.3. Especificación de las pruebas
      Para este proyecto se han diseñado tres niveles de pruebas:
      
      • Pruebas unitarias: Verifican el funcionamiento aislado de las 
        funciones clave del sistema, como la gestión de IDs, carga y guardado
        de datos, y operaciones CRUD.
        
      • Pruebas de integración: Validan el comportamiento del sistema cuando
        múltiples componentes interactúan, como por ejemplo el flujo completo
        de crear un libro y luego visualizarlo.
        
      • Pruebas de aceptación: Evalúan la aplicación desde la perspectiva
        del usuario final, utilizando la interfaz web y verificando que todas
        las funcionalidades son accesibles y funcionan correctamente.
        
      [Incluir tablas detalladas de casos de prueba]
   
   3.4. Plan de Pruebas
      [Insertar plan completo con referencias al anexo en Excel]
   
   3.5. Ejecución de las pruebas
      3.5.1. Entorno de pruebas
         • Sistema Operativo: Linux (Fedora 41)
         • Python: 3.13.2
         • Dependencias: Flask 3.1.0, pytest 8.3.5, pytest-cov 6.1.1
         • Navegador: Chrome/Firefox última versión
      
      3.5.2. Procedimiento de ejecución
         Para ejecutar la aplicación:
         ```bash
         # Crear y activar entorno virtual
         python -m venv venv
         source venv/bin/activate
         
         # Instalar dependencias
         pip install -r requirements.txt
         
         # Ejecutar la aplicación
         python app.py
         ```
         
         Para ejecutar las pruebas:
         ```bash
         # Pruebas unitarias con cobertura
         cd test
         pytest -v --cov=../app --cov=../books test_*.py --cov-report=html
         
         # Generar reporte HTML
         pytest --html=report.html
         ```
         
      3.5.3. Resultados y análisis
         • Tasa de éxito: 9/9 pruebas pasadas
         • Cobertura de código: 88% global (93% app.py, 81% books.py)
         • Defectos encontrados: 0 bloqueantes, 0 críticos, 2 menores
         
         [Insertar gráficos de cobertura y resultados]
   
   3.6. Conclusión
      Las pruebas realizadas demuestran que la aplicación BookHaven cumple con 
      los requisitos funcionales básicos para la gestión de un catálogo de 
      libros. Las operaciones CRUD funcionan correctamente tanto desde la API 
      como desde la interfaz de usuario.
      
      La cobertura de código del 88% supera el objetivo mínimo del 85%, 
      aunque se identifican áreas de mejora en el módulo books.py.
      
      Se identificaron 2 defectos menores relacionados con la validación de 
      datos y la gestión de imágenes que no comprometen la funcionalidad 
      principal, pero que deberían ser corregidos en futuras iteraciones.

4. ANEXOS
   • Anexo 1: Plan de ejecución de pruebas (Excel)
   • Anexo 2: Evidencia de ejecución (archivo ZIP)
   • Anexo 3: Código fuente de las pruebas