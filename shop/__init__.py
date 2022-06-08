from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_msearch import Search

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

from shop.admin import routes
from shop.products import routes
from shop.carts import carts