from app import app
from app.models import Product

from flask_login import login_required, current_user
from flask import render_template, redirect, url_for


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/product/<int:id>')
@login_required
def product(id):
    try:
        if not Product.query.get(id):
            return render_template('404.html'), 404
    except:
        return render_template('404.html'), 404

    return render_template('product.html', id=id)