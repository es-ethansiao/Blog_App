from flask import render_template, url_for, flash, redirect
from main_app import app, db, bcrypt
from main_app.forms import RegistrationForm, LoginForm
from main_app.models import User, Post
from flask_login import login_user, current_user, logout_user

# ==================== LISTS AND DICTIONARIES OF BLOG POSTS ====================
# Blog posts send titles, authors, content, and date posted to homepage
posts = [
    
    {
        'author': 'Kimi Realon',
        'title': 'Blog Post 1',
        'content': 'This is my first post on this sh!tty blog app :D. HAHAHA I posted before @Ethan Siao',
        'date_posted': 'February 13, 2022'        
    },
    
    {
        'author': 'Ethan Siao',
        'title': 'Blog Post 2',
        'content': 'This is my first post on this sh!tty blog app :D F*ck you @Kimi Realon',
        'date_posted': 'February 14, 2022'        
    },
    
    {
        'author': 'Micro Ramos',
        'title': 'Blog Post 3',
        'content': 'This is my first post on this sh!tty blog app :D. NIGGER NIGGER NIGGER NIGGERS',
        'date_posted': 'February 14, 2022'        
    },
    
    {
        'author': 'Milan Taylor',
        'title': 'Blog Post 4',
        'content': 'This is my first post on this sh!tty blog app :D. fuck bitches get money',
        'date_posted': 'February 14, 2022'        
    },
    
]

# Routes for main/home page
@app.route("/")
@app.route("/home")
def home():
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # takes password from form and hashes it into utf to put into the database
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # takes data from form for a user
        db.session.add(user) # adds user information to database
        db.session.commit() # commits changes to database
        flash('Your account has been successfully created! You are now able to log in!', 'success') # Flash imported from flask displays temporary message
        return redirect(url_for('login')) # redirects user to the homepage
    return render_template('register.html', title='Register', form=form) # form=form creates a form which is set as above

# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm() # sets form to login form from the forms python file'
    if form.validate_on_submit(): # allows the form to validate upon submission
        user = User.query.filter_by(email=form.email.data).first() # query checks database for first email
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', title='Login', form=form) # form=form creates a form which is set as above

# Route for log out page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
