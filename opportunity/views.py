# Imports
from opportunity import app
from flask import render_template, make_response, url_for, send_file, abort

'''
Views
'''


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')