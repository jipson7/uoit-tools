from flask import Blueprint, render_template, request
from uoit_tools.models import Course, Day

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home_get():
    return render_template('index.html'), 200

@main.route('/roomfinder', methods=['GET'])
def find_rooms():
    find_date = request.args.get('date', None)
    print(find_date)
    return 'OK', 200
