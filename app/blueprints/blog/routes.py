from crypt import methods
from flask import current_app as app, render_template, request, redirect, url_for, flash
from .models import User
from flask_login import login_user, logout_user, current_user
from app import db
from .models import Post

# USER ROUTES
@app.route('/users')
def user_list():
    return render_template('users/list.html', users=[user for user in User.query.all() if user != current_user])

@app.route('/users/<int:id>')
def user_single(id):
    return 'User Single Page'

@app.route('/users/unfollow/<user_id>')
def unfollow(user_id):
    user_to_unfollow = User.query.get(user_id)
    current_user.unfollow(user_to_unfollow)
    db.session.commit()
    flash(f'You have unfollowed {user_to_unfollow.first_name} {user_to_unfollow.last_name}', 'primary')
    return redirect(url_for('user_list'))

@app.route('/users/follow/<user_id>')
def follow(user_id):
    user_to_follow = User.query.get(user_id)
    current_user.follow(user_to_follow)
    db.session.commit()
    flash(f'You have followed {user_to_follow.first_name} {user_to_follow.last_name}', 'primary')
    return redirect(url_for('user_list'))

# a => t45dr
# b => bdkzs
# c => gszdgl
# 1 => tesrg
# 2 => ksrtjhk
# 3 => gsjzd

# hash
# abc123 = t45drbdkzsgszdgltesrgksrtjhkksrtjhk

# salting
# abc123 => SHA1235-2wt90a7bf8yphljkTEGPUOqhuRp
# abc123 => SHA1235-nkawejlsgzbhuWG89uio2hqt34
# check_password('SHA1235-nkawejlsgzbhuWG89uio2hqt34', 'abc123')

@app.route('/users/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = request.form
        # cross-reference email address with our database to determine if it's found
        user = User.query.filter_by(email=form_data.get('email')).first()
        
        # check email and password's vailidity
        if user is None or not user.check_password(form_data.get('password')):
            flash('Either that email address or password is incorrect. Please try again.', 'warning')
            return redirect(url_for('login'))
        
        # log the user in
        login_user(user, remember=form_data.get('remember_me'))
        flash('You have logged in successfully', 'success')
        return redirect(url_for('home'))
    return render_template('users/login.html')

@app.route('/users/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form
        
        email = User.query.filter_by(email=form_data.get('email')).first()
        if email is not None:
            flash('That email address is already in use. Please try another one.', 'warning')
            return(redirect(url_for('register')))
        if form_data.get('password') == form_data.get('confirm_password'):
            # create new user
            user = User(
                first_name=form_data.get('first_name'),
                last_name=form_data.get('last_name'),
                email=form_data.get('email')
            )
            user.generate_password(form_data.get('password'))
            db.session.add(user)
            db.session.commit()

            # log in the user after they register
            login_user(user, remember=True)
            
            flash('You have registered successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash("Your passwords don't match. Please try again.", 'warning')
            return redirect(url_for('register'))
    return render_template('users/register.html')

@app.route('/users/logout')
def logout():
    logout_user()
    flash('You have logged out successfully', 'primary')
    return redirect(url_for('login'))

@app.route('/blog/update', methods=['POST'])
def blog_profile():
    if request.method == 'POST':
        data = request.form.get('blog_post')
        p = Post(body=data, author=current_user.get_id())
        db.session.add(p)
        db.session.commit()
        flash('You have created a new post', 'info')
        return redirect(url_for('profile'))