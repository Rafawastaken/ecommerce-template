from shop import db
from datetime import datetime
import json

from shop import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

# Register customer
class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = False)
    username = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(200), unique = False)
    country = db.Column(db.String(50), unique = False)
    # state = db.Column(db.String(50), unique = False)
    city = db.Column(db.String(50), unique = False)
    contact = db.Column(db.String(50), unique = False)
    address = db.Column(db.String(50), unique = False)
    zipcode = db.Column(db.String(50), unique = False)
    profile = db.Column(db.String(200), unique = False, default = 'profile.jpg')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.name

# Json encoded order
class JsonEncodeDict(db.TypeDecorator):
    impl = db.Text

    # Function names are forced
    def process_bind_param(self, value, dialect): # 
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    # Function names are forced
    def process_result_value(self, value, dialect): # 
        if value is None:
            return '{}'
        else:
            return json.loads(value)

# Customer order
class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    invoice = db.Column(db.String(20), unique = True, nullable = False)
    status = db.Column(db.String(20), nullable = False, default = 'Pending')
    customer_id = db.Column(db.Integer, unique = False, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    orders = db.Column(JsonEncodeDict)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice


db.create_all()