from wtforms import Form, StringField, BooleanField, PasswordField,SubmitField,validators, ValidationError
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from shop.models import UserCustomer




class CustomerRegisterForm(FlaskForm):
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])

    profile = FileField('Profile Pics', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if UserCustomer.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if UserCustomer.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")

class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

