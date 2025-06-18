from flask import Flask, request, render_template, redirect, url_for
import os
from books import agregar_producto, load_products, eliminar_producto, actualizar_producto

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/imgs'

os.makedirs('data', exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    productos = load_products()
    return render_template('home.html', productos=productos.values())

@app.route('/home')
def home():
    return render_template('home.html', productos=load_products().values())

@app.route('/categoria/<categoria>')
def filtrar_por_categoria(categoria):
    productos = load_products()
    productos_filtrados = {
        codigo: producto for codigo, producto in productos.items()
        if producto.get('categoria') == categoria
    }
    return render_template('home.html', productos=productos_filtrados.values())

@app.route('/admin')
def admin():
    productos = load_products()
    return render_template('admin.html', productos=productos)

@app.route('/add_product', methods=['POST'])
def add_product():
    titulo = request.form['titulo']
    autor = request.form['autor']
    descripcion_completa = request.form['descripcion_completa']
    stock = int(request.form['stock'])
    precio = float(request.form['precio'])
    categoria = request.form['categoria']
    image = request.files['image']

    imagen_nombre = ""
    if image and image.filename:
        imagen_nombre = image.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen_nombre)
        image.save(image_path)

    agregar_producto(titulo, autor, descripcion_completa, stock, precio, imagen_nombre, categoria)
    return redirect(url_for('admin'))

@app.route('/edit_product/<codigo>')
def edit_product(codigo):
    productos = load_products()
    if codigo in productos:
        return render_template('edit_product.html', producto=productos[codigo])
    return redirect(url_for('admin'))

@app.route('/update_product/<codigo>', methods=['POST'])
def update_product(codigo):
    productos = load_products()
    if codigo in productos:
        titulo = request.form['titulo']
        autor = request.form['autor']
        descripcion_completa = request.form['descripcion_completa']
        stock = int(request.form['stock'])
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        
        imagen_nombre = productos[codigo].get('imagen', '')
        image = request.files['image']
        if image and image.filename:
            imagen_nombre = image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen_nombre)
            image.save(image_path)
            
        actualizar_producto(codigo, titulo, autor, descripcion_completa, stock, precio, imagen_nombre, categoria)
    
    return redirect(url_for('admin'))

@app.route('/delete_product/<codigo>')
def delete_product(codigo):
    eliminar_producto(codigo)
    return redirect(url_for('admin'))

@app.route('/book/<codigo>')
def book_detail(codigo):
    productos = load_products()
    if codigo in productos:
        return render_template('book_detail.html', libro=productos[codigo])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)