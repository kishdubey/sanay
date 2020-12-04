from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
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
