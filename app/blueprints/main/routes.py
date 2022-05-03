from flask import render_template, current_app as app

# MAIN APPLICATION ROUTES
@app.route('/')
def home():
    # raise Exception('This is a general exception I\'m trying to raise for no reason.')
    return render_template('main/home.html')

@app.route('/profile')
def profile():
    return render_template('main/profile.html')

@app.route('/contact')
def contact():
    return "Contact Page"