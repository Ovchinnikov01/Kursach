from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm, CSRFProtect  
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret key"

app.config['UPLOAD_FOLDER'] = 'static/product-images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATABASE = 'database.db' 

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('PRAGMA foreign_keys = ON')  
    return conn

def create_tables():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            image TEXT NOT NULL,
            price REAL NOT NULL
        );
    """)

    cursor.execute("SELECT * FROM product")
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO product (name, code, image, price) VALUES
            ('telofon', 'nokia', 'product-images/bag.jpg', 12000.00),
            ('telofon', 'nokia', 'product-images/external-hard-drive.jpg', 5000.00),
            ('nokia', 'nokia', 'static/product-images/shoes.jpg', 1000.00),
            ('nokia', 'nokia', 'static/product-images/laptop.jpg', 80000.00),
            ('nokia', 'nokia', 'static/product-images/camera.jpg', 150000.00),
            ('nokia', 'nokia', 'static/product-images/mobile.jpg', 3000.00),
            ('nokia', 'nokia', 'static/product-images/watch.jpg', 3000.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),  
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
             ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia1', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia2', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia3', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia4', 'nokia', 'static/product-images/tel.png', 400.00),
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00),                               
            ('nokia5', 'nokia', 'static/product-images/tel.png', 400.00);
                                            
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            profile_picture TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)

    db.commit()
    db.close()

create_tables()



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Пользователь с таким именем или электронной почтой уже существует')
        finally:
            db.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        db.close()

        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Неверный логин или пароль')
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'logged_in' in session and session['logged_in']:
        username = session['username']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        cursor.execute("SELECT * FROM orders WHERE username=?", (username,))
        orders = cursor.fetchall()

        order_details = []
        for order in orders:
            cursor.execute("SELECT product.*, order_items.quantity FROM product INNER JOIN order_items ON product.id = order_items.product_id WHERE order_items.order_id=?", (order[0],))
            products = cursor.fetchall()
            order_details.append((order, products))

        cursor.execute("SELECT * FROM product")
        all_products = cursor.fetchall()

        db.close()

        return render_template('profile.html', user=user, order_details=order_details, all_products=all_products)
    else:
        return redirect(url_for('login'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'logged_in' in session and session['logged_in']:
        username = session['username']
        cart_items = session.get('cart_item', {})
        total_price = session.get('all_total_price', 0.0)

        if request.method == 'POST':
            try:
                db = get_db()
                cursor = db.cursor()

               
                cursor.execute("INSERT INTO orders (username, total_price) VALUES (?, ?)", (username, total_price))
                order_id = cursor.lastrowid

                
                for code, item in cart_items.items():
                    cursor.execute("INSERT INTO order_items (order_id, code, quantity, price) VALUES (?, ?, ?, ?)",
                                   (order_id, item['code'], item['quantity'], item['price']))

                db.commit() 
                session.clear()

                flash('Заказ оформлен успешно!', 'success')
                return redirect(url_for('profile'))

            except sqlite3.Error as e:
                db.rollback() 
                flash(f'Ошибка оформления заказа: {e}', 'error')
                return redirect(url_for('checkout')) 
            finally:
                if db:
                    db.close() 

        else:
            return render_template('checkout.html', cart_items=cart_items, total_price=total_price)
    else:
        return redirect(url_for('login'))


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'logged_in' in session and session['logged_in']:
        username = session['username']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        db.close()

        if user:
            if request.method == 'POST':
                new_email = request.form['email']
                new_profile_picture = request.files.get('profile_picture')

                db = get_db()
                cursor = db.cursor()

                try:
                    if new_profile_picture:
                       
                        new_profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{username}.jpg'))
                        
                       
                        cursor.execute("UPDATE users SET email=?, profile_picture=? WHERE username=?", 
                                       (new_email, f'/static/profile_pictures/{username}.jpg', username))
                    else:
                        cursor.execute("UPDATE users SET email=? WHERE username=?", (new_email, username))

                    db.commit()
                    db.close()
                    return redirect(url_for('profile'))
                except sqlite3.IntegrityError:
                    db.close()
                    return render_template('edit_profile.html', user=user, error='Электронная почта уже используется')
                finally:
                    db.close()

            db.close()
            return render_template('edit_profile.html', user=user)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_product_to_cart():
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']

        if _quantity and _code and request.method == 'POST':
            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT * FROM product WHERE code=?", (_code,))
            row = cursor.fetchone()

            if row:
                
                image_file = request.files.get('image')
                if image_file and image_file.filename != '':
                    image_filename = image_file.filename
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    image_file.save(image_path)
                else:
                    image_filename = row[3]

                itemArray = {
                    _code: {
                        'name': row[1],
                        'code': row[2],
                        'quantity': _quantity,
                        'price': row[4],
                        'image': image_filename,
                        'total_price': _quantity * row[4]
                    }
                }

                
                all_total_price = 0
                all_total_quantity = 0

                session.modified = True
                if 'cart_item' in session:
                    if _code in session['cart_item']:
                        session['cart_item'][_code]['quantity'] += _quantity
                        session['cart_item'][_code]['total_price'] = session['cart_item'][_code]['quantity'] * row[4]
                    else:
                        session['cart_item'].update(itemArray)

                    for key, value in session['cart_item'].items():
                        all_total_quantity += int(value['quantity'])
                        all_total_price += float(value['total_price'])
                else:
                    session['cart_item'] = itemArray
                    all_total_quantity += _quantity
                    all_total_price += _quantity * row[4]

                session['all_total_quantity'] = all_total_quantity
                session['all_total_price'] = all_total_price

                db.close()
                return redirect(url_for('.products'))
            else:
                db.close()
                return 'Product not found'
        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(f"Error: {e}")
        return 'An error occurred'
    finally:
        pass

@app.route('/products')
def products():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM product")
        rows = cursor.fetchall()
        db.close()
        return render_template('products.html', products=rows)
    except Exception as e:
        print(e)
    finally:
        pass

@app.route('/cart') 
def cart():
    cart_items = session.get('cart_item', {})  
    total_quantity = session.get('all_total_quantity', 0)
    total_price = session.get('all_total_price', 0.0)
    return render_template('cart.html', cart_items=cart_items, total_quantity=total_quantity, total_price=total_price)

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)

@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        if 'cart_item' in session and code in session['cart_item']:
            session['cart_item'].pop(code, None)

            if 'cart_item' in session:
                for key, value in session['cart_item'].items():
                    all_total_quantity += int(value['quantity'])
                    all_total_price += float(value['total_price'])

        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        return redirect(url_for('.products'))
    except Exception as e:
        print(e)


@app.route('/admin_panel')
def admin_panel():
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM product")
            products = cursor.fetchall()
            products = [dict(zip([column[0] for column in cursor.description], row)) for row in products]
            db.close()
            return render_template('admin_panel.html', products=products)
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            if request.method == 'POST':
                name = request.form['name']
                code = request.form['code']
                price = request.form['price']
                image_file = request.files.get('image')

                if image_file and image_file.filename != '':
                    image_filename = image_file.filename
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    image_file.save(image_path)
                else:
                    return 'Ошибка: Загрузите изображение.'

                try:
                    db = get_db()
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO product (name, code, image, price) VALUES (?, ?, ?, ?)",
                                   (name, code, image_filename, price))
                    db.commit()
                    db.close()
                    flash('Товар добавлен успешно!', 'success')
                    return redirect(url_for('admin_panel'))
                except sqlite3.IntegrityError:
                    db.close()
                    return render_template('add_product.html', error='Товар с таким кодом уже существует')
            return render_template('add_product.html')
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/edit_product/<int:product_id>')
def edit_product(product_id):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM product WHERE id=?", (product_id,))
            product = cursor.fetchone()
            if product:
                product = dict(zip([column[0] for column in cursor.description], product))
                db.close()
                return render_template('edit_product.html', product=product)
            else:
                db.close()
                return 'Товар не найден.'
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/edit_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            name = request.form['name']
            code = request.form['code']
            price = request.form['price']
            image_file = request.files.get('image')

            db = get_db()
            cursor = db.cursor()

            if image_file and image_file.filename != '':
                image_filename = image_file.filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(image_path)
                cursor.execute("UPDATE product SET name=?, code=?, image=?, price=? WHERE id=?",
                               (name, code, image_filename, price, product_id))
            else:
                cursor.execute("UPDATE product SET name=?, code=?, price=? WHERE id=?",
                               (name, code, price, product_id))

            db.commit()
            db.close()
            flash('Товар изменен успешно!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/delet_product/<int:product_id>')
def delet_product(product_id):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute("DELETE FROM product WHERE id=?", (product_id,))
                db.commit()
                db.close()
                flash('Товар удален успешно!', 'success')
                return redirect(url_for('admin_panel'))
            except Exception as e:
                print(e)
                db.close()
                flash('Ошибка удаления товара', 'error')
                return redirect(url_for('admin_panel'))
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/orders')
def admin_orders():
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM orders")
            orders = cursor.fetchall()
            orders = [dict(zip([column[0] for column in cursor.description], row)) for row in orders]
            db.close()
            return render_template('admin_orders.html', orders=orders)
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/order/<int:order_id>/<string:action>', methods=['POST'])
def handle_order(order_id, action):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            db = get_db()
            cursor = db.cursor()

            if action == 'accept':
                cursor.execute("UPDATE orders SET status='Принят' WHERE id=?", (order_id,))
                db.commit()
                db.close()
                flash('Заказ принят в работу!', 'success')
            elif action == 'reject':
                cursor.execute("UPDATE orders SET status='Отклонен' WHERE id=?", (order_id,))
                db.commit()
                db.close()
                flash('Заказ отклонен!', 'success')
            elif action == 'complete':
                cursor.execute("UPDATE orders SET status='Завершен' WHERE id=?", (order_id,))
                db.commit()
                db.close()
                flash('Заказ завершен!', 'success')
            else:
                db.close()
                flash('Некорректное действие.', 'error')
            return redirect(url_for('admin_orders'))
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)