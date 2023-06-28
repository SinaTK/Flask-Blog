import wtforms 
from wtforms.validators import DataRequired, Length,  Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from flask_login import current_user
from blog.models import User


class RegisterForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[DataRequired(), Length(4, 30)])
    email = wtforms.StringField('Email', validators=[DataRequired(), Email()])
    password = wtforms.PasswordField('Password', validators=[DataRequired()])
    confirm_password = wtforms.PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This user name already exists.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already used to registeration.')

class LoginForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[DataRequired(), Length(4, 30)])
    password = wtforms.PasswordField('Password', validators=[DataRequired()])
    remember = wtforms.BooleanField('Remember me')


class EditProfileForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[DataRequired(), Length(4, 30)])
    email = wtforms.StringField('Email', validators=[DataRequired(), Email()])

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This user name already exists.')
        
    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email already used to registeration.')
            
class CreatePostForm(FlaskForm):
    title = wtforms.StringField('Post title', validators=[DataRequired(), Length(5, 250)])
    body = wtforms.TextAreaField('Post text', validators=[DataRequired()])


