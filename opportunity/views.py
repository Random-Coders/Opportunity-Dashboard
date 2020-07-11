# Imports
from opportunity import app, login_manager
from opportunity.dbmodels.oppmodel import Opportunity
from flask import render_template, make_response, url_for, send_file, abort
'''
Views
'''

@login_manager.user_loader
def load_user(id):
    return None


@app.route('/', methods=['GET'])
def index():
    opp = Opportunity()
    print(opp.add("opp_title","date", "img", "desc", "link", "topic", "author"))

    return render_template('home.html')