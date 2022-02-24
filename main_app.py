# ==================== BLOGGING APP allows users to view and post blogs with an account ====================

# This is a blog app the allows users to register and post blogs

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "695f4d33049851be2b077d9ffe1d8cf2"

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
@app.route("/login")
def login():
    form = LoginForm() # sets form to login form from the forms python file
    return render_template('login.html', title='Login', form=form) # form=form creates a form which is set as above

# Allows main app to run the web server
if __name__=='__main__':
    app.run(debug=True)
