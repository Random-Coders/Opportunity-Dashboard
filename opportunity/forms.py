from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


'''
Forms for jyl toolbox
'''


class LoginForm(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterUser(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Enter your name or organization"})
    password = PasswordField(
        'Password',
        validators=[
            Length(min=2),
            DataRequired(),
            EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password')
    submit = SubmitField('Create Account')

