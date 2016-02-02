import json, datetime, copy
from flask import Blueprint, request
from sqlalchemy import or_, not_
from uoit_tools.models import Course, Day
from dateutil import parser as date_parser
from datetime import timedelta, datetime
#Debuggy
from uoit_tools import db
from flask import jsonify

scheduler = Blueprint('scheduler', __name__)


@scheduler.route('/test', methods=['GET'])
def test_gres():
    query = db.session.query(Day.section_type.distinct().label("title"))
    titles = [row.title for row in query.all()]
    return jsonify({'result':titles}), 200


@scheduler.route('', methods=['POST'])
def create_schedules():
    f = request.form;
    semester = f.get('semester', None)
    names = f.getlist('courses[]', None)

    for name in names:
        courses = Course.query.\
            filter_by(course_code=name, semester=semester).all()
        types_added = []
        for course in courses:
            print(course.type)
    return 'OK', 200

@scheduler.route('/semesters', methods=['GET'])
def get_available_semesters():
    #This function needs to be finished with a query to the db.
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


class Schedule:

    M = []
    T = []
    W = []
    R = []
    F = []

    # Returns true if the add was a success, false otherwise
    def add_course(self, name, section):
        course = Course.query.filter_by(course_code=name, section=section).all()
