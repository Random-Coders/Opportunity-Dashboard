# Imports
from opportunity import app, login_manager, bcrypt
from opportunity.dbmodels.oppmodel import Opportunity
from opportunity.dbmodels.usermodel import User
from opportunity.forms import *
from opportunity.methods.issafe import is_safe_url
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime

'''
Views
'''


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)


@app.route('/', methods=['GET'])
def index(): 
    opp = Opportunity()
    opp.add("opp_title",datetime.now(), "img", "desc", "link", "topic", "author")
    return opp.load_spliced(3, 1)
    # return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = RegisterUser()
    if form.validate_on_submit():

        email = form.email.data
        title = form.title.data
        password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        find_user = User.get_by_email(email)

        if find_user is None:
            User.register(email, title, password)
            login_user(User.get_by_email(email))
            flash(f'Account created for {form.title.data}!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Account already exists for {form.title.data}!', 'success')

        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():

        user_log = User.get_by_email(form.email.data)

        if User.login_valid(form.email.data, form.password.data):
            loguser = User.get_by_email(form.email.data)
            login_user(loguser, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'warning')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))
