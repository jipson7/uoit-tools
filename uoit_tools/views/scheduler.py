import copy, json
from flask import Blueprint, request, jsonify
from uoit_tools.models import Course, Day
from dateutil import parser as date_parser
from datetime import datetime


scheduler = Blueprint('scheduler', __name__)


@scheduler.route('', methods=['POST'])
def create_schedules():
    f = request.form;
    semester = f.get('semester', None)
    names = f.getlist('courses[]', None)


    schedules = [Schedule()]
    errors = []

    for name in names:
        sections = Course.query.filter_by(course_code=name, semester=semester).all()
        if not sections:
            errors.append(name + ' was not found.')
        for course in sections:
            if course.type == 'Lecture':
                schedules = expandSchedules(schedules, course, course.days)
            else:
                for day in course.days:
                    schedules = expandSchedules(schedules, course, [day])
    data = {
        'schedules':[schedule.json() for schedule in schedules],
        'errors': errors
        }
    return jsonify(data), 200

def expandSchedules(schedules, course, days):
    return_schedules = []
    new_schedules = []
    for schedule in schedules:
        if schedule.contains_literal(days[0]):
            return_schedules.append(schedule)
        elif schedule.contains_type(course):
            return_schedules.append(schedule)
            new_schedule = schedule.copy()
            new_schedule.delete_slot(course)
            new_schedules.append(new_schedule)
        else:
            new_schedules.append(schedule.copy())
    for schedule in new_schedules:
        if schedule.add(days):
            return_schedules.append(schedule)
    return return_schedules

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
            if day.day not in ['M', 'T', 'W', 'R', 'F']:
                return False
            slot = {
                'name': day.course.course_code,
                'start': str(day.start_time),
                'end': str(day.end_time),
                'type': day.section_type,
                'day': day.day,
                'id': self._get_id(day),
                'reg': day.course.reg
            }
            if self.slot_overlaps(slot, day.day):
                return False
            else:
                slots.append(slot)
        for slot in slots:
            self.weekdays[slot['day']].append(slot)
        return True

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

    def delete_slot(self, course):
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
