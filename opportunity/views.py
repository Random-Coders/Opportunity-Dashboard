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
from urllib.parse import urlparse

'''
Views
'''


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)


@app.route('/', methods=['GET'])
def index():
    opp = Opportunity()
    opp.add("opp_title",datetime.now(), "img", "desc", "link", "coding", "author")
    # return opp.load_spliced(3, 1)
    comm = CommManager()
    comm.getleaders()

    #opp.add("hello",datetime.now(), "https://rafael.sirv.com/Images/rafael.jpeg", "desc hello", "https://rafael.cenzano.com", "topic", "Rafael Cenzano")
    posts = opp.load_recent_posts(10)
    return render_template('home.html', posts=posts, create=False)


@app.route('/create', methods=['GET'])
@login_required
def create():
    opp = Opportunity()
    posts = opp.load_recent_posts(10)
    return render_template('home.html', posts=posts, create=True)


@app.route('/create/post', methods=['GET', 'POST'])
@login_required
def creatingpost():
    form = CreateOpp()
    if form.validate_on_submit():

        urlCheck = urlparse(form.img.data)
        urlCheck0 = urlparse(form.link.data)
        if urlCheck.scheme and urlCheck.netloc and urlCheck0.scheme and urlCheck0.netloc and ('png' in form.img.data or 'jpg' in form.img.data or 'jpeg' in form.img.data or 'gif' in form.img.data or 'webp' in form.img.data):
            opp = Opportunity()
            result = opp.add(
                form.title.data,
                form.date.data,
                form.img.data,
                form.desc.data,
                form.link.data,
                form.topic.data,
                current_user['title'],
                current_user['_id'])
            print(form.topic.data)
            flash('Post created successfully', 'success')
            return redirect(url_for('opportunityPost', _id=result.inserted_id))
        flash('Error with creation. Link or image might not be a valid link', 'warning')
        return render_template('postCreate.html', form=form)

    #form.topic.choices = [(row['_id'], row['topic']) for row in State.query.all()]
    form.topic.choices = [('choice','choice'),('choice2','choice2')]
    form.date.data = datetime.now()
    return render_template('postCreate.html', form=form, community=False, current_user=current_user)


@app.route('/create/post/<community_id>', methods=['GET', 'POST'])
@login_required
def creatingpostcommunity(community_id):
    form = CreateOpp()
    if form.validate_on_submit():

        urlCheck = urlparse(form.img.data)
        urlCheck0 = urlparse(form.link.data)
        if urlCheck.scheme and urlCheck.netloc and urlCheck0.scheme and urlCheck0.netloc and ('png' in form.img.data or 'jpg' in form.img.data or 'jpeg' in form.img.data or 'gif' in form.img.data or 'webp' in form.img.data):
            opp = Opportunity()
            result = opp.add(
                form.title.data,
                form.date.data,
                form.img.data,
                form.desc.data,
                form.link.data,
                community_id,
                current_user['title'],
                current_user['_id'])
            flash('Post created successfully', 'success')
            return redirect(url_for('opportunityPost', _id=result.inserted_id))
        flash('Error with creation. Link or image might not be a valid link', 'warning')
        return render_template('postCreate.html', form=form)

    form.date.data = datetime.now()
    return render_template('postCreate.html', form=form, community=True, current_user=current_user)


@app.route('/opportunity/<_id>', methods=['GET'])
def opportunityPost(_id):
    try:
        opp = Opportunity()
        # find opp post by id
        post = connect('opportunity').opps.find({"_id" : ObjectId(_id)}).limit(1)[0]
        if post:
            return render_template('post.html', post=post)    
        raise BaseException
    except:
        flash('Post not found', 'error')
        return redirect(url_for('index'))


@app.route('/posts', methods=['GET'])
def posts():

    opp = Opportunity()

    posts, size = opp.load_spliced(0, 9)
    
    return render_template('posts.html', posts=posts, start=0)


@app.route('/posts/<start>', methods=['GET'])
def postsMore(start):
    opp = Opportunity()
    posts, size = opp.load_spliced(start, 9)
    if posts:
        return render_template('posts.html', posts=posts, start=start)
    return redirect(url_for('posts'))


@app.route('/test')
def test():
    # comm = CommManager()
    # comm.create("second climber", "climb higher", "coding")
    # print(comm.getleaders())

    opp = Opportunity()
    opp.add(
        "hello",
        datetime.now(),
        "https://rafael.sirv.com/Images/rafael.jpeg",
        "desc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hellodesc hello",
        "https://rafael.cenzano.com",
        "topic",
        "Rafael Cenzano")
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
