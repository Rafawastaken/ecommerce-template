from typing import Text
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = IntegerField('Price', [validators.DataRequired()])
    discount = IntegerField('Price', [validators.DataRequired()])
    stock = IntegerField('Price', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators = [FileRequired(), FileAllowed(['jpg', 'png', 'gif']), 'Images Only'])
    image_2 = FileField('image 2', validators = [FileRequired(), FileAllowed(['jpg', 'png', 'gif']), 'Images Only'])
    image_1 = FileField('Image 3', validators = [FileRequired(), FileAllowed(['jpg', 'png', 'gif']), 'Images Only'])