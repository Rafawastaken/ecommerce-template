from ast import Pass
from itertools import zip_longest
from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField
from wtforms import validators
from flask_wtf.file import FileRequired, FileAllowed, FileField

class CustomerRegisterForm(Form):
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
    state = StringField('State: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    zipcode = StringField('Zip Code: ', [validators.DataRequired()])

    # Profile Image
    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'bmp', 'jpeg'], 'Format Unkonwn')])

    # Submit
    submit = SubmitField('Register')