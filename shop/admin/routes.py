from flask import render_template, session, url_for, redirect, request, flash

# System imports
import os

# Local imports
from shop import app, db, bcrypt
from shop.products.models import Addproduct, Brand, Category
from .forms import RegistrationForm, LoginForm
from .models import User

#  Landing Admin
@app.route("/admin")
def admin():
    # Check if user is authenticated
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    # Query products
    products = Addproduct.query.all()
    return render_template('admin/index.html', title = 'Admin Page', products = products)

# Display brands
@app.route('/brands')
def brands():
    # Check if user is authenticated
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    # Query brands
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title = 'Brand Page', brands = brands)

# Display categories
@app.route('/categories')
def categories():
    # Check if user is authenticated
    if 'email' not in session:
        flash("Please log in first", 'danger')
        return redirect(url_for('login'))
    # Query categories
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title = 'Category Page', categories = categories)


# Register users
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Registration Form
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Create hash 
        hash_password = bcrypt.generate_password_hash(form.password.data)

        # Add user to database
        user = User(
            name = form.name.data,
            username = form.username.data,
            email = form.email.data,
            password = hash_password,
            profile = "profie.jpg"
        )

        db.session.add(user)
        db.session.commit()

        flash(f'Welcome {user.name}! Thanks for registering', 'success')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form, title = "Register Page")

# Login Page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Login Form
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Try to query user form input
        user = User.query.filter_by(email = form.email.data).first()

        # Validate Users input
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Add Email to session
            session['email'] = form.email.data
            flash(f"Welcome back {user.name}! You are logged", 'success')
            return redirect(request.args.get('next') or url_for('admin'))

        flash('Passowrd is incorrect. Please try again.', 'danger')
    return render_template('admin/login.html', form = form, title = "Login Page")

# Clear Session
@app.route('/logout')
def logout():
    session.clear()
    return "logged out"
