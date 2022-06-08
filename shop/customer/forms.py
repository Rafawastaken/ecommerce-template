from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, ValidationError
from wtforms import validators
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm

from .models import Register

# Register Form
class CustomerRegisterForm(FlaskForm):
    # Singup info
    name = StringField('Name: ', [validators.DataRequired()])
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [
        validators.Email(),
        validators.DataRequired()
    ])

    password = PasswordField('Password: ', [
        validators.DataRequired(), validators.EqualTo('confirm', message="Passwords don't match")
    ])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])

    # Address Info
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    zipcode = StringField('Zip Code: ', [validators.DataRequired()])

    # Profile Image
    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'bmp', 'jpeg'], 'Format Unkonwn')])

    # Submit
    submit = SubmitField('Register')

    
    # Check if username is valid to be added
    def validate_username(self, username):
        if Register.query.filter_by(username = username.data).first():
            raise ValidationError("Username already exists")

    def validate_email(self, email):
        if Register.query.filter_by(email = email.data).first():
            raise ValidationError("Email is already in use")


# Login Form
class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
    submit = SubmitField('Login')