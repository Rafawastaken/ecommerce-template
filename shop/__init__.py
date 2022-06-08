from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_msearch import Search
from flask_login import LoginManager

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# App Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "randompasswordtemporaria"
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

# Upload images
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

# App Modules
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Search Module
search = Search()
search.init_app(app)

# Login Manager
login_manager = LoginManager()  
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u'Please, Login First'

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customer import routes