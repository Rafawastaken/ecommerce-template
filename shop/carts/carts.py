from math import prod
from operator import sub
from statistics import quantiles
from flask import redirect, render_template, request, url_for, flash, session, current_app
from importlib_metadata import method_cache

from shop import db, app
from shop.products.models import Addproduct

# Merge Items in Shoppingcart Session
def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

# Method to add to cart
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id = product_id).first()

        if product_id and quantity and colors and request.method == "POST":
            DictItems = {
                product_id:{
                    'name':product.name,
                    'price':product.price,
                    'discount':product.discount,
                    'color':colors,
                    'quantity':quantity,
                    'stock':product.stock,
                    'image':product.image_1,
                    'colors':product.colors
                    }
                }
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("Product already in cart") # Change to increment.
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)

                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

# Display cart
@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal = subtotal + float(product['price']) * int(product['quantity'])
        subtotal = subtotal - discount 
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('products/carts.html', title = "Cart", tax = tax, grandtotal = grandtotal)

# Update Cart
@app.route('/updatecart(<int:code>', methods=['POST'])
def updatecart(code):
    # If shopping cart doesnt exist or is empty
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash("Product updated with success!", 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            flash('Something went wrong', 'danger')
            return redirect(url_for('getCart'))

# Delete cart
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))
    