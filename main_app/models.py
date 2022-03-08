from datetime import datetime
from main_app import db, login_manager
from flask_login import UserMixin

# ==================== CLASSES (DATABASE TABLES) AND COLUMNS FROM DATABASE ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # query gets user id and makes sure it is an integer

# Database class for user details
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False) # false null makes some sort of imput compulsory
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # default profile picture is set if there's nothing
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) # relationship (two way) pulls out information from User or Post class
    
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
