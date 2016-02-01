import json, datetime
from flask import Blueprint, request
from sqlalchemy import or_, not_
from uoit_tools.models import Course, Day
from dateutil import parser as date_parser
from datetime import timedelta, datetime

scheduler = Blueprint('scheduler', __name__)

@scheduler.route('', methods=['POST'])
def create_schedules():
    f = request.form;
    semester = f.get('semester', None)
    courses = f.getlist('courses[]', None)
    print(courses)
    print(semester)
    return 'OK', 200

@scheduler.route('/semesters', methods=['GET'])
def get_available_semesters():
    semesters = {
        'January (Winter) 2016': '201601',
        'September (Fall) 2015': '201509'
    }
    data = {
        'semesters': semesters,
        'current': get_semester_code()
    }
    return json.dumps(data), 200


def get_semester_code(d=datetime.now()):
    if d.month < 5:
        m = '01'
    elif d.month < 9:
        m = '05'
    else:
        m = '09'
    return str(d.year) + m

def get_day_code(d):
    codes = ['M', 'T', 'W', 'R', 'F']
    i = d.weekday()
    if i < 5:
        return codes[i]
