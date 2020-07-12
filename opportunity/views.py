# Imports
from opportunity import app, login_manager, bcrypt
from opportunity.dbmodels.oppmodel import Opportunity
from opportunity.dbmodels.usermodel import User
from opportunity.dbmodels.manager import connect
from opportunity.forms import *
from opportunity.methods.issafe import is_safe_url
from opportunity.dbmodels.commmodel import CommManager
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime
from bson.objectid import ObjectId

'''
Views
'''


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)


@app.route('/', methods=['GET'])
def index(): 
    opp = Opportunity()
    # opp.add("opp_title",datetime.now(), "img", "desc", "link", "climbings", "author")
    # return opp.load_spliced(3, 1)
    comm = CommManager()
    comm.getleaders()

    #opp.add("hello",datetime.now(), "https://rafael.sirv.com/Images/rafael.jpeg", "desc hello", "https://rafael.cenzano.com", "topic", "Rafael Cenzano")
    posts = opp.load_recent_posts(10)
    return render_template('home.html', posts=posts, create=False)


@app.route('/create', methods=['GET'])
def create():
    opp = Opportunity()
    posts = opp.load_recent_posts(10)
    return render_template('home.html', posts=posts, create=True)


@app.route('/opportunity/<_id>', methods=['GET'])
def opportunityPost(_id):
    opp = Opportunity()
    posts = opp.load_all()

    # find opp post by id
    post = connect('opportunity').opps.find({"_id" : ObjectId(_id)}).limit(1)[0]
    if post:
        return render_template('post.html', post=post) 

    flash('Post not found', 'error')
    return redirect(url_for('index'))


@app.route('/test')
def test():
    comm = CommManager()
    comm.create("hackathon", "code", "climbing")
    # opp = Opportunity()
    # opp.add("hello",datetime.now(), "https://rafael.sirv.com/Images/rafael.jpeg", "desc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hello", "https://rafael.cenzano.com", "topic", "Rafael Cenzano")
    return redirect(url_for('index'))

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
        name = form.name.data
        password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        find_user = User.get_by_email(email)

        if find_user is None:
            User.register(email, name, password)
            login_user(User.get_by_email(email))
            flash(f'Account created for {form.name.data}!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Account already exists for {form.name.data}!', 'success')

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
