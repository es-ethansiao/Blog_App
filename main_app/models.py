from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main_app import db, login_manager, app
from flask_login import UserMixin

# ==================== CLASSES (DATABASE TABLES) AND COLUMNS FROM DATABASE ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # query gets user id and makes sure it is an integer

# Database class for user details
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(30), unique=True, nullable=False) # false null makes some sort of imput compulsory
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # default profile picture is set if there's nothing
    posts = db.relationship('Post', backref='author', lazy=True) # relationship (two way) pulls out information from User or Post class
    
    def get_reset_token(self, expires_sec=1800): # reset token expires in 30 mins (default value set up for below)
        s = Serializer(app.config['SECRET_KEY'], expires_sec) # variable s sets up serializer and secret key from init
        # returning of s dumps into a token and the payload is within dumps and decoded into utf-8
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod # doesn't change and makes sure function doesn't expect 'self'
    def verify_reset_token(token): # verifying reset token when it has been used
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id'] # loads token to see if user_id is obtained
        except:
            # if token doesn't exist, invalid, or time has run out, return none (nothing happens)
            return None
        # if token is verified, enter database to get user_id
        return User.query.get(user_id)
    
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
