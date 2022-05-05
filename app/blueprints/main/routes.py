from flask import render_template, current_app as app, request, redirect, url_for, flash
from datetime import datetime as dt
from app.blueprints.blog.models import Post, User
from app import db, mail
from flask_login import current_user
from flask_mail import Message

# MAIN APPLICATION ROUTES
@app.route('/', methods=['GET', 'POST'])
def home():
    # if current_user.is_authenticated:
    #     print(current_user.is_authenticated)
    #     print(current_user.is_anonymous)
    #     print(current_user.is_active)
    #     print(current_user.get_id())
    # control what happens on a form submission/POST request
    if request.method == 'POST':
        # grab form data
        data = request.form.get('blog_post')

        # create new post
        p = Post(body=data, author=current_user.get_id())
        
        # stage post to be committed to the database
        db.session.add(p)

        # send that/those change(s) to the database
        db.session.commit()

        flash('You have created a new post', 'info')
        return redirect(url_for('home'))
    # raise Exception('This is a general exception I\'m trying to raise for no reason.')
    return render_template('main/home.html', posts=[post.to_dict() for post in current_user.followed_posts().all()])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        form_data = request.form

        # update the user's information
        user = User.query.get(current_user.get_id())
        # if the user wants to change their password
        # check if the (confirm) password fields are the same
        user.first_name = form_data.get('first_name')
        user.last_name = form_data.get('last_name')
        user.email = form_data.get('email')

        if len(form_data.get('password')) == 0:
            pass
        elif form_data.get('password') == form_data.get('confirm_password'):
            user.generate_password(form_data.get('password'))
        else:
            flash('There was an error updating your password', 'danger')
            return redirect(url_for('profile'))

        db.session.commit()
        # print(form_data.get('first_name'))
        # print(form_data.get('last_name'))
        # print(form_data.get('email'))
        # print(form_data.get('password'))
        # print(form_data.get('confirm_password'))
        flash('You have updated your information', 'primary')
        return redirect(url_for('profile'))
    return render_template('main/profile.html', posts=[post.to_dict() for post in Post.query.filter_by(author=current_user.get_id()).order_by(Post.date_created.desc()).all()])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        form_data = request.form
        msg = Message(
            subject='[Fakebook March] Contact form inquiry',
            recipients=[app.config.get('MAIL_RECIPIENT')],
            sender=app.config.get('MAIL_RECIPIENT'),
            # body=render_template('email/message.txt', data=form_data),
            html=render_template('email/message.html', data=form_data),
            reply_to=form_data.get('email'),
        )
        mail.send(msg)
        flash('Thank you for your inquiry. Please give us 48 hours to get back to you.', 'success')
        return redirect(request.referrer)
    return render_template('main/contact.html')

# OBJECT RELATIONAL MAPPER

# class Post:
#     id
#     body

# SQL - post => id, body, date_created