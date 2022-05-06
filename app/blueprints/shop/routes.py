from flask import current_app as app, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
import stripe
from .models import Cart
from app import db

stripe.api_key = app.config.get('STRIPE_SK')

# SHOP ROUTES
@app.route('/shop')
@login_required
def shop_list():
    products = []
    for product in stripe.Product.list()['data']:
        price = stripe.Price.retrieve(product['default_price'])['unit_amount'] / 100

        product_dict = {
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'price': f"{price:,.2f}",
            'image': product['images'][0],
        }
        products.append(product_dict)
    return render_template('shop/list.html', products=products)

# @app.route('/shop/2q483yq4958327')
@app.route('/shop/<id>')
@login_required
def shop_single(id):
    return 'Shop Single Page'

@app.route('/shop/cart')
@login_required
def shop_cart():
    cart_items = []
    for item in Cart.query.filter_by(user_id=current_user.get_id()).all():
        stripe_product = stripe.Product.retrieve(item.product_id)
        price = stripe.Price.retrieve(stripe_product['default_price'])['unit_amount'] / 100
        product_dict = {
            'info': stripe_product,
            'price': f"{price:,.2f}",
            'quantity': item.quantity
        }
        cart_items.append(product_dict)
    return render_template('shop/cart.html', cart=cart_items)

@app.route('/shop/cart/add/<product_id>')
@login_required
def shop_cart_add(product_id):
    user_cart = Cart.query.filter_by(user_id=current_user.get_id())
    cart_product = user_cart.filter_by(product_id=product_id).first()
    
    # if user doesn't already have a cart
    if cart_product is None:
        # create their cart
        cart = Cart(
            product_id=product_id, 
            user_id=current_user.get_id(),
            quantity=1 
        )
        db.session.add(cart)
    # if user has a cart and has the item already in it
    else:
        # if the same product has already been found in the cart
        cart_product.quantity += 1
    db.session.commit()
          
    flash('You have added that product successfully', 'primary')
    return redirect(url_for('shop_list'))

@app.route('/shop/checkout', methods=['POST'])
@login_required
def shop_checkout():
    items = []
    user_cart = Cart.query.filter_by(user_id=current_user.get_id()).all()
    for item in user_cart:
        stripe_product = stripe.Product.retrieve(item.product_id)
        product_dict = {
            'price': stripe_product['default_price'],
            'quantity': item.quantity
        }
        items.append(product_dict)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            success_url='https://fakebook-march-2022.herokuapp.com/shop/cart',
            cancel_url='https://fakebook-march-2022.herokuapp.com/shop/cart',
        )

        # upon successful payment, remove all items from user's cart
        for item in user_cart:
            db.session.delete(item)
        db.session.commit()
        flash('Your payment was successful. Thank you for shopping!', 'success')
    except Exception as e:
        flash('Your payment was unsuccessful. Please try again!', 'danger')
        return str(e)
    return redirect(checkout_session.url)
