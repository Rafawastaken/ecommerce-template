import profile
from flask import render_template, session, url_for, redirect, request, flash

# System imports
import os

# Local imports
from .forms import RegistrationForm, LoginForm
from .models import User
from shop import app, db, bcrypt


@app.route("/")
def admin():
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/index.html', title = 'Admin Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)

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

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        print("Teste")
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            print("Logged in")
            flash(f"Welcome back {user.name}! You are logged", 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        flash('Passowrd is incorrect. Please try again.', 'danger')
    return render_template('admin/login.html', form = form, title = "Login Page")

@app.route('/logout')
def logout():
    session.clear()
    return "logged out"