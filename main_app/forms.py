from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main_app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        # queries database to check if there is already a username in the database
        user = User.query.filter_by(username=username.data).first() 
        if user:
            raise ValidationError('That username is already taken! Please choose another one.')
    
    def validate_email(self, email):
        # queries database to check if there is already an email in the database
        user = User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('That email is already taken! Please choose another one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    def validate_username(self, username):
        if username.data != current_user.username:
            # queries database to check if there is already a username in the database
            user = User.query.filter_by(username=username.data).first() 
            if user:
                raise ValidationError('That username is already taken! Please choose another one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            # queries database to check if there is already an email in the database
            user = User.query.filter_by(email=email.data).first() 
            if user:
                raise ValidationError('That email is already taken! Please choose another one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class ReportForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'readonly': True})
    sportteam = StringField('Sport/Team', validators=[DataRequired()])
    details = TextAreaField('Details', validators=[DataRequired()])
    submit = SubmitField('Send')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        # queries database to check if there is already an email in the database
        user = User.query.filter_by(email=email.data).first() 
        if user is None: # checking to see if there is an email is there or not
            # raises message requesting registration because there is no email with the account
            raise ValidationError('There is no account with that email. You need to register first.')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
