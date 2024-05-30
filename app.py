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

app.config['DATABASE'] = 'database.db'


db = sqlite3.connect(app.config['DATABASE'], check_same_thread=False)
cursor = db.cursor()


def create_tables():
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
    db.commit()

create_tables()
def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            profile_picture TEXT
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Пользователь с таким именем или электронной почтой уже существует')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

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
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template('profile.html', user=user)
        else:
            return redirect(url_for('login'))
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
                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()

                
                cursor.execute("INSERT INTO orders (username, total_price) VALUES (?, ?)", (username, total_price))
                order_id = cursor.lastrowid

                
                for code, item in cart_items.items():
                    cursor.execute("INSERT INTO order_items (order_id, code, quantity, price) VALUES (?, ?, ?, ?)",
                                   (order_id, item['code'], item['quantity'], item['price']))

                conn.commit()  
                session.clear()

                
                flash('Заказ оформлен успешно!', 'success')
                return redirect(url_for('profile'))

            except sqlite3.Error as e:
                
                conn.rollback()  
                flash(f'Ошибка оформления заказа: {e}', 'error')
                return redirect(url_for('checkout'))  
            finally:
                if conn:
                    conn.close()  

        else:
            
            return render_template('checkout.html', cart_items=cart_items, total_price=total_price)
    else:
        return redirect(url_for('login'))
    

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'logged_in' in session and session['logged_in']:
        username = session['username']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            if request.method == 'POST':
                new_email = request.form['email']
                new_profile_picture = request.files.get('profile_picture')

                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()

                try:
                    if new_profile_picture:
                        
                        new_profile_picture.save(os.path.join(app.root_path, 'static', 'profile_pictures', f'{username}.jpg'))
                        
                        cursor.execute("UPDATE users SET email=?, profile_picture=? WHERE username=?", (new_email, f'/static/profile_pictures/{username}.jpg', username))
                    else:
                        cursor.execute("UPDATE users SET email=? WHERE username=?", (new_email, username))

                    conn.commit()
                    return redirect(url_for('profile'))
                except sqlite3.IntegrityError:
                    return render_template('edit_profile.html', user=user, error='Электронная почта уже используется')
                finally:
                    conn.close()

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
                return redirect(url_for('.products'))  
            else:
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
        cursor.execute("SELECT * FROM product")
        rows = cursor.fetchall()
        return render_template('products.html', products=rows)
    except Exception as e:
        print(e)
    finally:
        pass


@app.route('/cart') 
def view_cart():
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


def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False

@app.route('/admin_panel')
def admin_panel():
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            return render_template('admin_panel.html')
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
                    cursor.execute("INSERT INTO product (name, code, image, price) VALUES (?, ?, ?, ?)",
                                   (name, code, image_filename, price))
                    db.commit()
                    flash('Товар добавлен успешно!', 'success')
                    return redirect(url_for('admin_panel'))
                except sqlite3.IntegrityError:
                    return render_template('add_product.html', error='Товар с таким кодом уже существует')
            return render_template('add_product.html')
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            cursor.execute("SELECT * FROM product WHERE id=?", (product_id,))
            product = cursor.fetchone()
            if product:
                if request.method == 'POST':
                    name = request.form['name']
                    code = request.form['code']
                    price = request.form['price']
                    image_file = request.files.get('image')

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
                    flash('Товар изменен успешно!', 'success')
                    return redirect(url_for('admin_panel'))
                return render_template('edit_product.html', product=product)
            else:
                return 'Товар не найден.'
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/delet_product/<int:product_id>')
def delet_product(product_id):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            try:
                cursor.execute("DELETE FROM product WHERE id=?", (product_id,))
                db.commit()
                flash('Товар удален успешно!', 'success')
                return redirect(url_for('admin_panel'))
            except Exception as e:
                print(e)
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
            cursor.execute("SELECT * FROM orders")
            orders = cursor.fetchall()
            return render_template('admin_orders.html', orders=orders)
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/order/<int:order_id>/<string:action>')
def handle_order(order_id, action):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            if action == 'accept':
                cursor.execute("UPDATE orders SET status='Принят' WHERE id=?", (order_id,))
                db.commit()
                flash('Заказ принят в работу!', 'success')
            elif action == 'reject':
                cursor.execute("UPDATE orders SET status='Отклонен' WHERE id=?", (order_id,))
                db.commit()
                flash('Заказ отклонен!', 'success')
            elif action == 'complete':
                cursor.execute("UPDATE orders SET status='Завершен' WHERE id=?", (order_id,))
                db.commit()
                flash('Заказ завершен!', 'success')
            else:
                flash('Некорректное действие.', 'error')
            return redirect(url_for('admin_orders'))
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)