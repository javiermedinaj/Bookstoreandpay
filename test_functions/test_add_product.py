import sys
import os

# Añadir el directorio padre al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from books import agregar_producto, load_products

def test_string_price_and_stock():
    """Test adding a product with string price and stock"""
    # Add a product with string values
    result = agregar_producto(
        "Libro con Precio String",
        "Autor de Prueba",
        "Descripción del libro con precio string",
        "diez",  # String stock
        "precio en texto",  # String price
        "test.jpg",
        "Fiction"
    )
    
    # Print the result
    print(f"Producto agregado con código: {result}")
    
    # Verify the product was added with string values
    productos = load_products()
    if result in productos:
        product = productos[result]
        print(f"Precio: {product['precio']}")
        print(f"Stock: {product['stock']}")
        assert product["precio"] == "precio en texto"
        assert product["stock"] == "diez"
        print("Test pasado: los valores string se mantuvieron")
    else:
        print("Error: Producto no encontrado")
        assert False

if __name__ == "__main__":
    test_string_price_and_stock()