from flask import render_template, current_app as app
from datetime import datetime as dt
from app.blueprints.blog.models import Post

# MAIN APPLICATION ROUTES
@app.route('/')
def home():
    # raise Exception('This is a general exception I\'m trying to raise for no reason.')
    return render_template('main/home.html', posts=[post.to_dict() for post in Post.query.all()])

@app.route('/profile')
def profile():
    return render_template('main/profile.html')

@app.route('/contact')
def contact():
    return "Contact Page"

# OBJECT RELATIONAL MAPPER

# class Post:
#     id
#     body

# SQL - post => id, body, date_created