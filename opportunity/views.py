# Imports
from opportunity import app, login_manager
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