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

'''
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=150,
                message='Password must be within 6 and 150 characters')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
'''


class RegisterUser(FlaskForm):
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


class CreatePost(FlaskForm):
    title = StringField(
        'Title', validators=[
            DataRequired(), Length(
                max=30, message='First name must be 30 characters or less')])
    description = TextAreaField(
        'Description', widget=[TextArea],
            validators=[
            DataRequired(), Length(
                max=30, message='First name must be 30 characters or less')])

