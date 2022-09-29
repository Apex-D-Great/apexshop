from flask import render_template, request, redirect, url_for, session, flash
from shop import app, db
from .forms import RegisterForm, LoginForm, ProductForm
from werkzeug.security import generate_password_hash, check_password_hash
from shop.models import User, AddProduct, Brand, Category
from flask_login import login_user, logout_user, login_required, current_user
import secrets
import os


@app.route("/admin")
@login_required
def adminhome():
    products = AddProduct.query.all()
    return render_template('admin/index.html', title='Admin', products=products)

@app.route("/admin/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('admin/register.html', title='Register', form=form)
    return render_template('admin/register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'welcome {current_user.username}, you are now logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin/login.html', title='Login', form=form)

@app.route("/brand", methods=['GET', 'POST'])
@login_required
def brand():
    brand = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Brand Page', brand=brand)

@app.route("/category", methods=['GET', 'POST'])
@login_required
def category():
    category = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Brand Page', category=category)

#---------------------- editing and deletion section-------------------------------
@app.route("/brand/update/<int:id>", methods=['GET', 'POST'])
@login_required
def brand_update(id):
    brand = Brand.query.get_or_404(id)
    form = request.form.get('brand')
    if request.method == 'POST':
        brand.name = form
        flash('updated successfully', 'success')
        db.session.commit()
        return redirect(url_for('brand'))
    return render_template('admin/update.html', title='update brand', brand=brand)

@app.route("/brand/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def brand_delete(id):
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    return redirect(url_for('brand'))

@app.route("/category/update/<int:id>", methods=['GET', 'POST'])
@login_required
def category_update(id):
    category = Category.query.get_or_404(id)
    form = request.form.get('category')
    if request.method == 'POST':
        category.name = form
        flash('updated successfully', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('admin/update.html', title='update category', category=category)

@app.route("/category/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def category_delete(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('category'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

    
@app.route("/product/update/<int:id>", methods=['GET', 'POST'])
@login_required
def product_update(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = AddProduct.query.get_or_404(id)
    form = ProductForm()
    if request.method=='POST' and form.validate_on_submit():
        if form.image1.data:
            product.image1 = save_picture(form.image1.data)
        if form.image2.data:
            product.image2 = save_picture(form.image2.data)
        if form.image3.data:
            product.image3 = save_picture(form.image3.data)
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.desc = form.description.data
        product.colors = form.colors.data
        product.brand_id = request.form.get('brand')
        product.category_id = request.form.get('category')
        db.session.commit()
        flash(f'The brand {product.name} was updated successfully', 'success')
        return redirect(url_for('home'))
    form.name.data = product.name
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.desc
    form.colors.data = product.colors
    form.price.data = product.price
    return render_template('admin/product.html', title='update product',
    form=form, brands=brands, categories=categories, product=product)

@app.route("/product/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def product_delete(id):
    product = AddProduct.query.get_or_404(id)
    # image_file1 = url_for('static', filename='images/' + product.image1)
    # image_file2 = url_for('static', filename='images/' + product.image2)
    # image_file3 = url_for('static', filename='images/' + product.image3)
    
    # picture_path1 = os.path.join(app.root_path, image_file1)
    # picture_path2 = os.path.join(app.root_path, image_file2)
    # picture_path3 = os.path.join(app.root_path, image_file3)


    # os.remove(picture_path1)
    # os.remove(picture_path2)
    # os.remove(picture_path3)

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('home'))
# --------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for("login"))