from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[Length(min=4,max=30), DataRequired()])
    email_address = StringField('Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password:', validators=[Length(min=6,max=50), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Sign up')



class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[Length(min=4,max=30), DataRequired()])
    password = PasswordField('Password:', validators=[Length(min=6,max=50), DataRequired()])
    submit = SubmitField('Log in')