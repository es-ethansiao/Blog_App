import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from main_app import app, db, bcrypt
from main_app.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                            PostForm, 
                            RequestResetForm, ResetPasswordForm)
from main_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# ==================== ROUTES ====================

# Routes for main/home page
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int) # page is a request from the database to go to the first page
    # grabs all posts from database
    # queries posts from db while paginate allows us to split things into pages with 5 blog posts for each page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts) # sends in parameter for blog posts

# Route for about page
@app.route("/about")
def about():
    return render_template('about.html', title='About') # sends in parameter for title of the webpage

# Route for registration page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # redirects current user logged in to the home page
        return redirect(url_for('home'))
    form = RegistrationForm() # sets form to registration form from the forms python file
    if form.validate_on_submit(): # allows the form to validate upon submission
        # takes password from form and hashes it into utf to put into the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # takes data from form for a user
        db.session.add(user) # adds user information to database
        db.session.commit() # commits changes to database
        # Flash imported from flask displays temporary message informing the user that the new account has been created
        flash('Your account has been successfully created! You are now able to log in!', 'success') 
        return redirect(url_for('login')) # redirects user to the homepage
    return render_template('register.html', title='Register', form=form, legend='Join Today') # form=form creates a form which is set as above

# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm() # sets form to login form from the forms python file
    if form.validate_on_submit(): # allows the form to validate upon submission
        user = User.query.filter_by(email=form.email.data).first() # query checks database for first email
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # logging in after attempting to access account page will redirect to account page, otherwise, user is redirected to homepage
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', title='Login', form=form, legend='Log In') # form=form creates a form which is set as above

# Route for log out page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Function for picture pathway and saving
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # takes filename and extension and splits text
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # takes full path of the blog app folder
    picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)
    # set variable resizes profile picture to a perfect square of 125 pixels
    output_size = (125, 125)
    # opens form picture that is uploaded into form
    i = Image.open(form_picture)
    # thumbnail takes output size variable
    i.thumbnail(output_size)
    # saves profile pic into pathway
    i.save(picture_path)
    # returns picture file name
    return picture_fn

# Route for account details page
@app.route("/account", methods=['GET', 'POST'])
@login_required # user needs to be logged in to access this page
def account():
    form = UpdateAccountForm() # sets form to update details form from the forms python file
    if form.validate_on_submit(): # allows the form to validate upon submission
        if form.picture.data:
            # uses function to save new profile picture into folder pathway
            picture_file = save_picture(form.picture.data)
            # changes current username to what's filled in the form
            current_user.image_file = picture_file
        # changes current username to what's filled in the form
        current_user.username = form.username.data
        # changes current email to what's filled in the form
        current_user.email = form.email.data
        db.session.commit()
        # Flash imported from flask displays temporary message informing the user that the datails have been updated
        flash('Your account has been updated!', 'success')
        # Redirects user to the same page
        return redirect(url_for('account'))
    # GET gets (literally) something out of the database
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image file goes into static folder and grabs jpg image file in profile pics folder which has been set up in the database
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account Details', image_file=image_file, form=form, legend='Account Details')

# Route for creating new posts
@app.route("/post/new", methods=['GET', 'POST'])
@login_required # user needs to be logged in to access this page
def new_post():
    # this form variable takes the post form that is imported from the forms Python file for the page
    form = PostForm()
    if form.validate_on_submit(): # allows the form to validate upon submission
        # sets post variable with inputted title, content, and logged-in user
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        # adds post variable and saves it to database
        db.session.add(post)
        db.session.commit()
        # flash message informs user of successful post while redirecting them to home page
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# Route for individual posts
@app.route("/post/<int:post_id>") # integer for post id is unique for all posts
def post(post_id):
    post = Post.query.get_or_404(post_id) # get_or_404 either grabs post id or if none found, displays 404 error
    return render_template('post.html', title=post.title, post=post)

# Route for updating posts
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST']) # integer for post id is unique for all posts
@login_required # user needs to be logged in to access this page
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # get_or_404 either grabs post id or if none found, displays 404 error
    if post.author != current_user:
        abort(403) # 403 error restricts access to posts that don't belong to the user [FORBIDDEN AHHHHHHHHH]
    form = PostForm()
    if form.validate_on_submit(): # form updates upon validation and returns to individual post view
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        # flash message informs user of successful post while redirecting them to individual post page
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET': # form pre-populates with existing data
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

# Route for deleting posts
@app.route("/post/<int:post_id>/delete", methods=['POST']) # integer for post id is unique for all posts
@login_required # user needs to be logged in to access this page
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) # get_or_404 either grabs post id or if none found, displays 404 error
    if post.author != current_user:
        abort(403) # 403 error restricts access to posts that don't belong to the user [FORBIDDEN AHHHHHHHHH]
    db.session.delete(post) # now we proceed to the deleting of the post from the database
    db.session.commit()
    # flash message informs user of successful deletion while redirecting them to home page
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# Route for reset request page
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated: # user must be logged out to change their password
        return redirect(url_for('home'))
    form = RequestResetForm()
    return render_template('reset_request.html', title='Reset Password', form=form, legend='Reset Password')

# Route for reset password page
@app.route("/reset_password/<token>", methods=['GET', 'POST']) # brings in token sent to email address as link
def reset_token(token):
    if current_user.is_authenticated: # user must be logged out to change their password
        return redirect(url_for('home'))
    user = User.verify_reset_token(token) # taken and verified from models file
    if user is None: # if token doesn't exist or the timer runs out
        # flashes warning message and redirects user back to reset request page
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm
    return render_template('reset_token.html', title='Reset Password', form=form, legend='Reset Password')
