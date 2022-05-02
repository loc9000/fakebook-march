from app import app


# MAIN APPLICATION ROUTES
@app.route('/')
def home():
    return 'Home Page'

@app.route('/profile')
def profile():
    return 'Profile Page'

@app.route('/contact')
def contact():
    return "Contact Page"

# USER ROUTES
@app.route('/users')
def user_list():
    return 'Users Page'

@app.route('/users/<int:id>')
def user_single(id):
    return 'User Single Page'

# SHOP ROUTES
@app.route('/shop')
def shop_list():
    return 'Shop List Page'

# @app.route('/shop/2q483yq4958327')
@app.route('/shop/<id>')
def shop_single(id):
    return 'Shop Single Page'

@app.route('/shop/cart')
def shop_cart():
    return 'Shop Cart Page'

@app.route('/shop/checkout')
def shop_checkout():
    return 'Shop Checkout Page'

