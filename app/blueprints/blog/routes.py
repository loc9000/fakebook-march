from flask import current_app as app, render_template

# USER ROUTES
@app.route('/users')
def user_list():
    return 'Users Page'

@app.route('/users/<int:id>')
def user_single(id):
    return 'User Single Page'