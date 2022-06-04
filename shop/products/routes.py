from functools import reduce
from math import prod
from flask import redirect, render_template, url_for, flash, request, session

import secrets

from .forms import Addproducts
from .models import Brand, Category, Addproduct
from shop import db, app, photos

# Add Brands
@app.route('/addbrand', methods = ['GET', 'POST'])
def addbrand():
    if request.method == 'POST':
        # Query brand
        getbrand = request.form.get('brand').title()
        
        # Add brand to database
        brand = Brand(name = getbrand)
        db.session.add(brand)
        db.session.commit()

        flash(f"Brand: '{getbrand}' added to database!", "success")
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands = True, title = 'Add Brand')
    
# Update Brand
@app.route('/updatebrand/<int:id>', methods = ['POST', 'GET'])
def updatebrand(id):
    # Check if user is authenticated
    if 'email' not in session:
        flash("Please log in first", 'danger')
        return redirect(url_for('login'))

    update_brand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')

    # If form is submited, update.
    if request.method == 'POST':
        update_brand.name = brand
        db.session.commit()
        flash(f'Brand {brand} updated with success!', 'success')
        return redirect(url_for('brands'))    

    return render_template('products/updatebrand.html', title = 'Update Brand', update_brand = update_brand)

# Update Category
@app.route('/updatecategory/<int:id>', methods=['POST', 'GET'])
def updatecat(id):
    # Check if user is authenticated
    if 'email' not in session:
        flash("Please log in first", 'danger')
        return redirect(url_for('login'))

    update_cat = Category.query.get_or_404(id)
    cat = request.form.get('category')

    # if form is submited, update
    if request.method == 'POST':
        update_cat.name =  cat
        db.session.commit()

        flash(f'Category {cat} updated with success!', 'success')
        return redirect(url_for('categories'))

    return render_template('products/updatebrand.html', title = 'Update Category', update_cat = update_cat)

# Add Category
@app.route('/addcat', methods = ['GET', 'POST'])
def addcat():
    if request.method == 'POST':
        # Query category
        getcategory = request.form.get('category').title()

        # Add Category to database
        cat = Category(name = getcategory)
        db.session.add(cat)
        db.session.commit()

        flash(f"Category:'{getcategory}' added to database!", "success")
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', title = 'Add Category')

# Add Product
@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
        # Check if user is authenticated
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))

    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)

    if request.method == 'POST':
        # Get form data
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data

        # Request form -> Not in forms
        brand = request.form.get('brand')
        category = request.form.get('category')

        # Request form media and saves it with hash name
        image_1 = photos.save(request.files.get('image_1'), name = secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name = secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name = secrets.token_hex(10) + ".")

        # Add product to database
        product = Addproduct(
            name = name,
            price = price,
            discount = discount,
            stock = stock,
            colors = colors,
            desc = desc,
            brand_id = brand,
            category_id = category,
            image_1 = image_1,
            image_2 = image_2,
            image_3 = image_3
        )

        db.session.add(product)
        db.session.commit()

        flash(f'Product {name} added to store!', 'success')
        return redirect(url_for('admin'))
        
    return render_template('products/addproduct.html', 
        title = "Add Product Page", form = form, brands = brands, 
        categories = categories)

# Update Product
@app.route('/updateproduct/<int:id>', methods = ['GET', 'POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    
    # Query data
    categories = Category.query.all()
    brands = Brand.query.all()
    product = Addproduct.query.get_or_404(id)

    # Aux variables
    brand_id = request.form.get('brand')
    category_id = request.form.get('category')


    # if form is submitted
    if request.method == 'POST':
        # update product in database
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.brand_id = brand_id
        product.category_id = category_id
        product.colors = form.colors.data
        product.desc = form.description.data

        # save on database
        db.session.commit()

        flash(f"{product.name} updated with success!", 'success')
        return redirect(url_for('admin'))

        # Match values with form
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.desc

    return render_template('products/updateproduct.html', 
        title = "Update Product", form = form, product = product, 
        brands = brands, categories = categories)