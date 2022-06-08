from unicodedata import category
from flask import current_app, render_template, url_for, flash
from flask import redirect, request, session

# General imports
import secrets
import os

# Locals imports
from shop import db, app, photos, products, search, bcrypt
from .forms import CustomerRegisterForm
from .models import Register


# Register Customer Page
@app.route('/customer/register', methods = ['GET', 'POST'])
def custom_register():
    form = CustomerRegisterForm(request.form)
    if request.method == 'POST':
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(
            name = form.name.data,
            username = form.username.data,
            email = form.email.data,
            password = hash_password,
            country = form.country.data,
            state = form.state.data,
            city = form.city.data,
            address = form.address.data,
            zipcode = form.zipcode.data,
        )

        db.session.add(register)
        db.session.commit()

        flash(f"Welcome {form.name.data}", 'success')
        return redirect(url_for('home'))
    return render_template('customers/register.html', form = form)