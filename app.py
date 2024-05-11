# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite///base.db'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


@app.route('/create')
def create():
    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)