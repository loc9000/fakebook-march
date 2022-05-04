from flask import render_template, current_app as app, request, redirect, url_for, flash
from datetime import datetime as dt
from app.blueprints.blog.models import Post
from app import db

# MAIN APPLICATION ROUTES
@app.route('/', methods=['GET', 'POST'])
def home():
    # control what happens on a form submission/POST request
    if request.method == 'POST':
        # grab form data
        data = request.form.get('blog_post')

        # create new post
        p = Post(body=data, author='87fb0ac1612444e18536bce80dacc7b4')
        
        # stage post to be committed to the database
        db.session.add(p)

        # send that/those change(s) to the database
        db.session.commit()

        flash('You have created a new post', 'info')
        return redirect(url_for('home'))
    # raise Exception('This is a general exception I\'m trying to raise for no reason.')
    return render_template('main/home.html', posts=[post.to_dict() for post in Post.query.order_by(Post.date_created.desc()).all()])

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