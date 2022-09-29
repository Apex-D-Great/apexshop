from flask_login import UserMixin
from datetime import datetime
from shop import db, login_manager
import json

# user table
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    profile = db.Column(db.String(200), nullable=False, default='profile.jpg')
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<name: %r>" % self.username

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

class AddProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # a product can have many brands
    # while many brands can have similar proaducts (many to one relationship)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))
    # whenever i want to use the backref and i do "product.brands(i get access to all of the Brand table because
    # brand_id is just like doing Brand.query.get(id).all(), brand_id is a class instance itself
    # product.backref=Brand.query.get(id).all()=brand_id)"

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('category', lazy=True))

    image1 = db.Column(db.String(200))
    image2 = db.Column(db.String(200))
    image3 = db.Column(db.String(200))

    def __repr__(self):
        return "<name: %r>" % self.name


@login_manager.user_loader
def load_user(user_id):
    return UserCustomer.query.get(int(user_id))
class UserCustomer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(50), unique= False)
    email = db.Column(db.String(50), unique= True)
    password = db.Column(db.String(200), unique= False)
    country = db.Column(db.String(50), unique= False)
    # state = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    profile = db.Column(db.String(200), unique= False , default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.name

# this function remodifies our textarea and allows it to accept JSON object and function as one!
class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEncodedDict)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice


