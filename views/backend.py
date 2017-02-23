
from flask.blueprints import Blueprint
from flask import render_template

bd = Blueprint('index', __name__)


@bd.route('/')
def home():
    return render_template('index.html')
