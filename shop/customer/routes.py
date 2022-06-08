from flask import current_app, render_template, url_for, flash
from flask import redirect, request, session

from flask_login import login_required, current_user, logout_user, login_user

# General imports
import secrets
import os

# Locals imports
from shop import db, app, photos, products, search, bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register


# Register Customer Page
@app.route('/customer/register', methods = ['GET', 'POST'])
def custom_register():
    form = CustomerRegisterForm()

    if form.validate_on_submit():
        print("validate_on_submit")

        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(
            name = form.name.data,
            username = form.username.data,
            email = form.email.data,
            password = hash_password,
            country = form.country.data,
            city = form.city.data,
            address = form.address.data,
            zipcode = form.zipcode.data,
        )

        db.session.add(register)
        db.session.commit()

        flash(f"Welcome {form.name.data}", 'success')
        return redirect(url_for('home'))
    return render_template('customers/register.html', title = 'register', form = form)

# Login User
@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are logged in!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        else:
            flash('Incorrect email or password', 'danger')
            return redirect(url_for('customerLogin'))

    return render_template('customers/login.html',title = 'Login', form = form)

# Logout User
@app.route('/customer/logout')
def customer_logout():
    logout_user()
    flash("You are logged out!", 'success')
    return redirect(url_for('home'))