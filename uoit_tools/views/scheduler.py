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
    course = Course.query.filter_by(course_code='CSCI2020U').first()
    schedule = Schedule()
    schedule.add(course.days)
    return 'ok', 200
    #query = db.session.query(Day.section_type.distinct().label("title"))
    #titles = [row.title for row in query.all()]
    #return jsonify({'result':titles}), 200


@scheduler.route('', methods=['POST'])
def create_schedules():
    f = request.form;
    semester = f.get('semester', None)
    names = f.getlist('courses[]', None)

    schedules = [Schedule()]

    def expandSchedules(course, days):
        for schedule in schedules:
            if schedule.contains(course):
                schedules.append(schedule.copy_and_delete(course))
                continue
            if not schedule.add(days):
                schedules.remove(schedule)

    for name in names:
        sections = Course.query.filter_by(course_code=name, semester=semester).all()
        for course in sections:
            if course.type == 'Lecture':
                expandSchedules(course, course.days)
            else:
                for day in course.days:
                    expandSchedules(course, [day])

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


class Schedule:

    weekdays = {
        'M': [],
        'T': [],
        'W': [],
        'R': [],
        'F': []
    }

    # Returns true if the add was a success, false otherwise
    def add(self, days):
        for day in days:
            slot = {
                'name': day.course.course_code,
                'start': day.start_time,
                'end': day.end_time,
                'type': day.section_type
            }
            self.weekdays[day.day].append(slot)
        print(self.weekdays)

    # Check if the specific course type exists in schedule (i.e. lab or whatever)
    def contains(self, course):
        return False

    def copy_and_delete(self, course):
        #return a copy of the entire schedule with the specified course type deleted
        pass
