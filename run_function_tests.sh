#!/bin/bash

# Script para ejecutar las pruebas de funciones y mostrar logs detallados

echo "======================================================================"
echo "                   Ejecutando pruebas de funciones                    "
echo "======================================================================"

# Instalar dependencias si no están instaladas
echo "Verificando dependencias..."
pip install pytest pytest-html pytest-cov

# Crear carpeta para logs si no existe
mkdir -p logs

# Ejecutar todas las pruebas de funciones con logs detallados
echo "Ejecutando pruebas con logs detallados..."
python -m pytest test_functions/ -v -s --log-cli-level=DEBUG --html=test_functions_report.html

# Ejecutar pruebas con cobertura de código
echo "Ejecutando pruebas con análisis de cobertura..."
python -m pytest test_functions/ --cov=books --cov-report=term --cov-report=html:test_functions_coverage

echo "======================================================================"
echo "                      Pruebas finalizadas                             "
echo "======================================================================"
echo "Reportes generados:"
echo "- Reporte HTML: test_functions_report.html"
echo "- Cobertura HTML: test_functions_coverage/index.html"
echo "======================================================================"
