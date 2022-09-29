from flask_login import login_required
from flask import render_template, request, redirect, url_for, flash
from shop import app, db
from flask_login import current_user
from shop.models import Brand, Category, AddProduct
from .forms import ProductForm, SearchForm
import secrets
import os



def brands():
    # the line below means for Brands that have Products attached to them,  join them (brand->products) together in an imaginary table
    brands = Brand.query.join(AddProduct, (Brand.id == AddProduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(AddProduct,(Category.id == AddProduct.category_id)).all()
    return categories

@app.context_processor
def base():
    return dict(brands=brands(), categories=categories(), form=SearchForm())



@app.route('/')
def home():
    page = request.args.get('page',1, type=int)
    products = AddProduct.query.filter(AddProduct.stock > 0).order_by(AddProduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products)


@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1, type=int)
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = AddProduct.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)
    return render_template('products/index.html',brand=brand,get_brand=get_brand)


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = AddProduct.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html',get_cat_prod=get_cat_prod,get_cat=get_cat)

@app.route('/product/<int:id>')
def single_page(id):
    product = AddProduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product)

# search route
@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    products = AddProduct.query
    if form.validate_on_submit():
        # get data from the form
        searchs = form.searched.data
        # query the database
        products = products.filter(AddProduct.name.like('%' + searchs + '%'))
        products = products.order_by(AddProduct.name).all()
        return render_template('products/search.html', products=products)



@app.route("/add_brand", methods=['GET', 'POST'])
def addbrand():
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        check_brand = Brand.query.filter_by(name=getbrand).first()
        if check_brand:
            flash(f'The brand {getbrand} already exist in your database', 'danger')
            return redirect(url_for('addbrand'))
        else:
            brand = Brand(name=getbrand)
            db.session.add(brand)
            db.session.commit()
            flash(f'The brand {getbrand} was added to your database', 'success')
            return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', title='add_brand', brands='brands')

@app.route("/add_category", methods=['GET', 'POST'])
def addcategory():
    if request.method == 'POST':
        getcat = request.form.get('category')
        check_cat = Category.query.filter_by(name=getcat).first()
        if check_cat:
            flash(f'The category {getcat} already exist in your database', 'danger')
            return redirect(url_for('addcategory'))
        else:
            category = Category(name=getcat)
            db.session.add(category)
            db.session.commit()
            flash(f'The brand {getcat} was added to your database', 'success')
            return redirect(url_for('addcategory'))
    return render_template('products/addbrand.html', title='add_category')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)

    # output_size = (125, 125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)


    return picture_fn

@app.route('/add_product', methods=['GET','POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = ProductForm()
    if request.method=='POST' and form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        description = form.description.data
        colors = form.colors.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image1 = save_picture(form.image1.data)
        image2 = save_picture(form.image2.data)
        image3 = save_picture(form.image3.data)
        add_pro = AddProduct(name=name, price=price, discount=discount, stock=stock,
        colors=colors, desc=description, brand_id=brand, category_id=category, image1=image1,
        image2=image2, image3=image3)
        db.session.add(add_pro)
        db.session.commit()
        flash(f'The brand {name} was added to your database', 'success')
        return redirect(url_for('home'))
    return render_template('products/addproduct.html', title='Add Product Page', 
    form=form, brands=brands, categories=categories)

# invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/error404.html"), 404

# internal server error
@app.errorhandler(500)
def server_error(e):
    return render_template("error/error500.html"), 500