import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from main_app import app, db, bcrypt
from main_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from main_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# ==================== ROUTES ====================

# Routes for main/home page
@app.route("/")
@app.route("/home")
def home():
    # grabs all posts from database
    posts = Post.query.all()
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
    return render_template('register.html', title='Register', form=form) # form=form creates a form which is set as above

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
    return render_template('login.html', title='Login', form=form) # form=form creates a form which is set as above

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
    return render_template('account.html', title='Account Details', image_file=image_file, form=form)

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
    return render_template('create_post.html', title='New Post', form=form)
