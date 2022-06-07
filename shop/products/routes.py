from unicodedata import category
from flask import current_app, render_template, url_for, flash
from flask import redirect, request, session
import secrets

# System imports
import os

# Locals imports
from .forms import Addproducts
from .models import Brand, Category, Addproduct
from shop import db, app, photos


################ CONSTs #################
PER_PAGE = 8

################# HELPERS #################
def brands(): # Query brands
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories(): # Query categories
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories

################# FRONTEND #################

# Homepage
@app.route('/')
def home():
    page = request.args.get('page', 1, type = int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page = page, per_page = PER_PAGE)
    return render_template('products/index.html', title="Ecom - Homepage", 
        products = products, brands = brands(), categories = categories())

# Products single page
@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)    
    return render_template('products/single_page.html', title=product.name ,product = product, 
        brands = brands(), categories = categories())

# Display Brands 
@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type = int)
    get_d = Brand.query.filter_by(id = id).first_or_404()
    brand = Addproduct.query.filter_by(brand_id = id).paginate(page = page, per_page = PER_PAGE)
    brand_name = Brand.query.filter_by(id = id).first().name
    
    return render_template('products/index.html', title = f'Watching {brand_name}',
        brand = brand, brands = brands(), categories =  categories(), get_d = get_d)

# Display Categories
@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type = int)
    get_cat = Category.query.filter_by(id = id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category = get_cat).paginate(page = page, per_page = PER_PAGE)
    category_name = Category.query.filter_by(id = id).first().name

    return render_template('products/index.html', title = f'Watching {category_name}',
        get_cat_prod = get_cat_prod, categories = categories(), brands = brands(), get_cat = get_cat)


################# BRANDS #################

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

# Delete Brand
@app.route('/deletebrand/<int:id>', methods = ['POST'])
def deletebrand(id):
    # Query brand
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        # Remove brand from database
        db.session.delete(brand)
        db.session.commit()
        flash(f"{brand.name} deleted from database", 'success')
        return redirect(url_for('admin'))

    # if request methods isn't POST
    flash(f"{brand.name} can't be deleted", 'warning')
    return redirect(url_for('admin'))

################# CATS #################

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

# Delete Category
@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    # Query category to delete
    cat = Category.query.get_or_404(id)
    if request.method == "POST":
        # Remove category from database
        db.session.delete(cat)
        db.session.commit()
        
        flash(f"{cat.name} deleted from database", 'success')
        return redirect(url_for('admin'))

    # if request methods isn't POST
    flash(f"{cat.name} can't be deleted", 'warning')
    return redirect(url_for('admin'))

################# PRODS #################

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

        # Replace images if image is found
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name = secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name = secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name = secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name = secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name = secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name = secrets.token_hex(10) + ".")

        # save database
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

# Delete Product
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    # Query product
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        # Delete Images
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
        except Exception as e:
            print(e)

        # Delete product database
        db.session.delete(product)
        db.session.commit()

        flash(f"{product.name} was deleted", 'success')
        return redirect(url_for('admin'))
    flash(f"Can't delete {product.name}", "danger")
    return redirect(url_for('admin'))