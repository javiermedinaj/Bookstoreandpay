# Pruebas de Funciones Individuales

Esta carpeta contiene pruebas unitarias para cada función principal del sistema de tienda de libros.

## Estructura

- `test_add_product.py`: Pruebas para añadir productos al catálogo
- `test_get_product.py`: Pruebas para obtener productos por código o listar todos
- `test_update_product.py`: Pruebas para actualizar información de productos
- `test_delete_product.py`: Pruebas para eliminar productos
- `test_filter_by_category.py`: Pruebas para filtrar productos por categoría
- `test_file_upload.py`: Pruebas para la carga de imágenes de portada

## Ejecutar las pruebas

Para ejecutar todas las pruebas con logs detallados:

```bash
./run_function_tests.sh
```

Esto ejecutará las pruebas mostrando los logs detallados y generará:
1. Un reporte HTML con los resultados de las pruebas
2. Un análisis de cobertura de código

## Ver logs específicos

Para ejecutar una prueba específica y ver sus logs:

```bash
# Ejecutar solo las pruebas de añadir producto
python -m pytest test_functions/test_add_product.py -v -s --log-cli-level=DEBUG

# Ejecutar un test específico
python -m pytest test_functions/test_add_product.py::test_add_product_success -v -s --log-cli-level=DEBUG
```

## Niveles de log

Puedes ajustar el nivel de detalle de los logs:

- `DEBUG`: Información muy detallada (valores, variables, etc.)
- `INFO`: Información general sobre el progreso de las pruebas
- `WARNING`: Advertencias que no impiden la ejecución
- `ERROR`: Errores que causan fallos en las pruebas
- `CRITICAL`: Errores graves que impiden la ejecución

## Notas

Estas pruebas están diseñadas para ejecutarse de forma independiente y restaurar el estado del sistema después de cada ejecución, para no interferir con los datos reales.
