# Imports
from opportunity import app, login_manager
from opportunity.forms import *
from flask import render_template, make_response, url_for, send_file, abort

'''
Views
'''

@login_manager.user_loader
def load_user(id):
    return None


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', form=form)