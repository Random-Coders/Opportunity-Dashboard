from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Length, Email

class CreateUserForm(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Enter your name or organization"})
    password = PasswordField(
        'Password',
        [
            Length(min=2),
            DataRequired(),
            EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password')
    submit = SubmitField('Create Account')