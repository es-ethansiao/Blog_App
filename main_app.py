# ==================== BLOGGING APP allows users to view and post blogs with an account ====================

# This is a blog app the allows users to register and post blogs

from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Secret key required to encrypt user passwords and input
app.config['SECRET_KEY'] = "695f4d33049851be2b077d9ffe1d8cf2"

# SQLAlchemy configuration for database that passes argument called app (as mentioned above)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # 3 /'s for route redirectory
db = SQLAlchemy(app)

# ==================== CLASSES (DATABASE TABLES) AND COLUMNS FROM DATABASE ====================
# Database class for user details
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False) # false null makes some sort of imput compulsory
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # default profile picture is set if there's nothing
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lasy=True) # backref creates author, while lasy loads info from database when needed
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')" # returns user class

# Database class for blog post details
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # imported from datetime, sets date and time of post to that instant
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')" # returns post class

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
    form = RegistrationForm() # sets form to registration form from the forms python file
    if form.validate_on_submit(): # allows the form to validate upon submission
        flash(f'Account Created for {form.username.data}!', 'success') # Flash imported from flask displays temporary message
        return redirect(url_for('home')) # redirects user to the homepage
    return render_template('register.html', title='Register', form=form) # form=form creates a form which is set as above

# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm() # sets form to login form from the forms python file'
    if form.validate_on_submit(): # allows the form to validate upon submission
        if form.email.data == 'admin@blog.com' and form.password.data == 'password': # Ensures below tasks are only done if email/pass combination is correct
            flash('You have been logged in!', 'success') # Flash imported from flask displays successful login
            return redirect(url_for('home')) # Redirects user to homepage
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', title='Login', form=form) # form=form creates a form which is set as above

# Allows main app to run the web server
if __name__=='__main__':
    app.run(debug=True)
