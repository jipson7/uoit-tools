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
    #course = Course.query.filter_by(course_code='CSCI2020U').first()
    #schedule = Schedule()
    #schedule.add(course.days)
    days = Day.query.filter(not_(Day.day.in_(('M', 'T', 'W', 'R', 'F'))))\
            .filter(Day.section_type=='Lecture').all()
    for d in days:
        print(d.course.course_code)
    return 'ok', 200


@scheduler.route('', methods=['POST'])
def create_schedules():
    f = request.form;
    semester = f.get('semester', None)
    names = f.getlist('courses[]', None)

    schedules = [Schedule()]

    for name in names:
        print(len(schedules))
        sections = Course.query.filter_by(course_code=name, semester=semester).all()
        for course in sections:
            if course.type == 'Lecture':
                schedules = expandSchedules(schedules, course, course.days)
            else:
                for day in course.days:
                    schedules = expandSchedules(schedules, course, [day])
    if schedules:
        print([schedule.json() for schedule in schedules])
    else:
        print('fuckin nothing')
    return 'OK', 200

def expandSchedules(schedules, course, days):
    print('expanding')
    old_schedules = []
    new_schedules = []
    for schedule in schedules:
        if schedule.contains_literal(days[0]):
            old_schedules.append(schedule)
        elif schedule.contains_type(course):
            old_schedules.append(schedule)
            new_schedule = schedule.copy()
            new_schedule.delete(course)
            new_schedules.append(new_schedule)
        else:
            new_schedules.append(schedule)
    for schedule in new_schedules:
        try:
            schedule.add(days)
        except ValueError as e:
            print(e)
            new_schedules.remove(schedule)
    return new_schedules + old_schedules

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

    def _get_id(self, day):
        return day.course.course_code + day.section_type + day.day + str(day.start_time)

    def add(self, days):
        slots = []
        for day in days:
            #if day.section_type not in ['M', 'T', 'W', 'R', 'F']:
            #    print('day is bad')
            #    return False
            slot = {
                'name': day.course.course_code,
                'start': day.start_time,
                'end': day.end_time,
                'type': day.section_type,
                'day': day.day,
                'id': self._get_id(day)
            }
            if self.slot_overlaps(slot, day.day):
                raise ValueError('Cannot add day to schedule')
            else:
                slots.append(slot)
        for slot in slots:
            self.weekdays[slot['day']].append(slot)

    def slot_overlaps(self, slot, day):
        weekday = self.weekdays[day]
        for existing in weekday:
            if (slot['start']>=existing['start'] and slot['start']<existing['end'])\
                or (slot['end']>existing['start'] and slot['end']<=existing['end']):
                return True
        return False

    def contains_literal(self, day):
        unique_id = self._get_id(day)
        for day, slots in list(self.weekdays.items()):
            for slot in slots:
                if slot['id'] == unique_id:
                    return True
        return False

    # Check if the specific course type exists in schedule (i.e. lab or whatever)
    def contains_type(self, course):
        for day, slots in list(self.weekdays.items()):
            for slot in slots:
                if course.course_code == slot['name'] and \
                    course.type == slot['type']:
                    return True
        return False

    def delete(self, course):
        for day, slots in list(self.weekdays.items()):
            for slot in slots:
                if course.course_code == slot['name'] and \
                    course.type == slot['type']:
                    self.weekdays[day].remove(slot)

    def json(self):
        return self.weekdays

    def copy(self):
        s = Schedule()
        s.weekdays = copy.deepcopy(self.weekdays)
        return s
