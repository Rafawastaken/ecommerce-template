from unicodedata import category
from flask import current_app, render_template, url_for, flash
from flask import redirect, request, session

# General imports
import secrets
import os

# Locals imports
from shop import db, app, photos, products, search
from .forms import CustomerRegisterForm


# Register Customer Page
@app.route('/customer/register', methods = ['GET', 'POST'])
def custom_register():
    form = CustomerRegisterForm(request.form)
    return render_template('customers/register.html', form = form)