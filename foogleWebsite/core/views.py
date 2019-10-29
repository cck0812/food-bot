from flask import render_template, request, Blueprint
from datetime import datetime
from flask_moment import Moment
# from foogleWebsite import app

core = Blueprint('core', __name__)
# moment = Moment(app)


@core.route('/')
def index():
    return render_template('index.html')



@core.route('/info')
def info():
    return render_template('info.html')


@core.route('/data')
def data():
    return render_template('data.html')
