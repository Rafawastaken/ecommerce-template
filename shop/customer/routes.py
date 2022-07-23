from operator import sub
from flask import current_app, render_template, url_for, flash
from flask import redirect, request, session

from flask_login import login_required, current_user, logout_user, login_user

# General imports
import secrets
import os

# Locals imports
from shop import db, app, photos, products, search, bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register, CustomerOrder


################# CUSTOMERS FUNCS #################

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

################# ORDERS #################

# Get Order 
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(
                invoice = invoice,
                customer_id = customer_id,
                orders = session['Shoppingcart'] # Session items in cart
            )

            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart') # Clear session cart after inserted
            flash("Your order has been submited!", 'success')
            return redirect(url_for('home'))

        except Exception as e:
            print(e)
            flash("Something went wrong while getting order", 'danger')
            return(redirect(url_for('getCart')))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandtotal = 0
        subtotal = 0
        discount = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id = customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id = customer_id).order_by(CustomerOrder.id.desc()).first()

        for key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            tax = ("%.2f" % (.06 * float(subtotal)))
            grandtotal = float("%.2f" % (1.06 * subtotal))
    else:
        return redirect(url_for('customerLogin'))

    return render_template("customers/order.html", title = "order", invoice = invoice, subtotal = subtotal, 
        grandtotal = grandtotal, tax = tax, customer = customer, orders = orders, discount = discount)