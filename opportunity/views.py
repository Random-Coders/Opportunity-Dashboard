# Imports
from opportunity import app, login_manager
from opportunity.dbmodels.oppmodel import Opportunity
from opportunity.dbmodels.usermodel import User
from opportunity.models.loginform import LoginForm
from opportunity.models.signupform import CreateUserForm
from opportunity.methods.issafe import is_safe_url
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect
from flask_login import login_required, login_user, current_user

'''
Views
'''

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)


@app.route('/', methods=['GET'])
def index():
    print(current_user)
    #opp = Opportunity()
    #print(opp.add("opp_title","date", "img", "desc", "link", "topic", "author"))

    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = CreateUserForm()
    if form.validate_on_submit():
        print("hello", form.email.data)

        email = form.email.data
        title = form.title.data
        password = form.password.data # not encrypting it bc don't know how; can change but not that important

        user = User(email, title, password)
        user.save_to_mongo()

        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user, remember=True)

        flash('Signed up successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index'))
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
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
