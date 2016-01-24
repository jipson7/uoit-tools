from flask import Blueprint, render_template, request
from uoit_tools.models import Course, Day
from dateutil import parser as date_parser

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home_get():
    return render_template('index.html'), 200

@main.route('/roomfinder', methods=['GET'])
def find_rooms():
    date_string = request.args.get('date', None)
    find_date = date_parser.parse(date_string)
    print(find_date)
    return 'OK', 200
