from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, TextAreaField, SelectField
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
    name = StringField(
        'Name',
        validators=[
            DataRequired()],
        render_kw={
            "placeholder": "Enter your name or organization"})
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(
                min=6,
                message='Password must be over 6 characters long'),
            EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password')
    submit = SubmitField('Sign up')


class CreateOpp(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            Length(
                max=30,
                message='Title should be 30 characters or less')])
    img = StringField('Image url', validators=[DataRequired()],
                      render_kw={
        "placeholder": "Enter an image url"})
    date = DateTimeField('Start Time', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    link = StringField('Link')
    topic = SelectField('Community')
    submit = SubmitField('Submit')


class ConfirmPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')
