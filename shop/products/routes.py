from flask import redirect, render_template, url_for, flash, request

from .models import Brand, Category
from shop import db, app

# Add Brands
@app.route('/addbrand', methods = ['GET', 'POST'])
def addbrand():
    if request.method == 'POST':
        getbrand = request.form.get('brand').title()
        brand = Brand(name = getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f"Brand: '{getbrand}' added to database!", "success")
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands = True, title = 'Add Brand')

# Add Category
@app.route('/addcat', methods = ['GET', 'POST'])
def addcat():
    if request.method == 'POST':
        getcategory = request.form.get('category').title()
        cat = Category(name = getcategory)
        db.session.add(cat)
        db.session.commit()
        flash(f"Category:'{getcategory}' added to database!", "success")
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', title = 'Add Category')