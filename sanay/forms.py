from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256 as sha256

from models import User

def invalid_credentials(form, field):
    """Username and Password Checker"""
    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or Password is incorrect")
    elif not sha256.verify(password_entered, user_object.password):
        raise ValidationError("Wrong Password!")

class RegistrationForm(FlaskForm):
    """Registration Form"""
    username = StringField('username_label',
        validators=[InputRequired(message="Username Required"),
        Length(min=4, max=25, message="Between 4 and 25 characters")])

    password = PasswordField('password_label',
            validators=[InputRequired(message="Password Required"),
            Length(min=4, max=25, message="Between 4 and 25 characters")])

    confirm_pswd = PasswordField('confirm_pswd_label',
            validators=[InputRequired(message="Password Required"),
            EqualTo('password', message="Passwords must match")])

    submit_button = SubmitField('Register')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists!")

class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('username_label', validators=[InputRequired(message="Username Required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password Required"), invalid_credentials])
    submit_button = SubmitField('Login')
