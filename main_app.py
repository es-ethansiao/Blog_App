# ==================== BLOGGING APP allows users to view and post blogs with an account ====================

# Importing templates from flask installed on device
from flask import Flask, render_template, url_for

# Importing forms from forms python file
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'fe8232dd0a2b9a7760b5978790a9884e'


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

app = Flask(__name__)

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
@app.route("/register")
def register():
    form = RegistrationForm() # sets form to registration form from the forms python file
    return render_template('register.html', title='Register', form=form) # form=form creates a form which is set as above

# Route for login page
@app.route("/login")
def login():
    form = LoginForm() # sets form to login form from the forms python file
    return render_template('login.html', title='Login', form=form) # form=form creates a form which is set as above

# Allows main app to run the web server
if __name__=='__main__':
    app.run(debug=True)
