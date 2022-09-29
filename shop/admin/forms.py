from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from flask_wtf import FlaskForm
from shop.models import User
from flask_wtf.file import FileRequired, FileField, FileAllowed

# registeration form
class RegisterForm(FlaskForm):
    def validate_username(self, user_to_check):
        user = User.query.filter_by(username=user_to_check.data).first()
        if user:
            raise ValidationError("username already exist, try another username")
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError("email already exist, try another email")
    username = StringField(label="Name" , validators=[DataRequired()])
    email = StringField(label="Email" , validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Submit")

# login form
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
   
    name = StringField(label="Name" , validators=[DataRequired()])
    price = DecimalField(label="Price" , validators=[DataRequired()])
    discount = IntegerField(label="Discount", default=0)
    stock = IntegerField(label="Stock" , validators=[DataRequired()])
    description = TextAreaField(label="Description" , validators=[DataRequired()])
    colors = TextAreaField(label="Colors" , validators=[DataRequired()])
    image1 = FileField('image 1', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image2 = FileField('image 2', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image3 = FileField('image 3', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    submit = SubmitField(label="Add Product")