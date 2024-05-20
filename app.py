from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  


if not os.path.exists('static/profile_pictures'):
    os.makedirs('static/profile_pictures')


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

create_table()

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
def home():
    return render_template('home.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0')