import copy, json, collections
from flask import Blueprint, request, jsonify
from uoit_tools.models import Course, Day
from dateutil import parser as date_parser
from datetime import datetime, timedelta


scheduler = Blueprint('scheduler', __name__)


@scheduler.route('', methods=['POST'])
def create_schedules():
    f = request.form;
    semester = f.get('semester', None)
    names = f.getlist('courses[]', None)

    schedules = {Schedule()}

    for name in names:
        sections = Course.query.filter_by(course_code=name, semester=semester).all()
        if not sections:
            return name + ' was not found in course list, remove it and try again.', 400
        for course in sections:
            if course.type == 'Lecture':
                schedules = expandSchedules(schedules, course, course.days)
            else:
                for day in course.days:
                    schedules = expandSchedules(schedules, course, [day])
    result = [x.json() for x in schedules]
    if not result:
        return 'No possible schedules exist for this combination of courses.', 404
    data = {
        'schedules': result,
        'firstSunday': get_first_sunday(semester)
        }
    return jsonify(data), 200

def expandSchedules(schedules, course, days):
    return_schedules = set()
    new_schedules = []
    for schedule in schedules:
        if schedule.contains_literal(days[0]):
            return_schedules.add(schedule)
        elif schedule.contains_type(course):
            return_schedules.add(schedule)
            new_schedule = schedule.copy()
            new_schedule.delete_slot(course)
            new_schedules.append(new_schedule)
        else:
            new_schedules.append(schedule)
    for schedule in new_schedules:
        if schedule.add(days):
            return_schedules.add(schedule)
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


class Schedule:

    def __init__(self):
        self.weekdays = {
            'M': [],
            'T': [],
            'W': [],
            'R': [],
            'F': []
        }

    def _get_id(self, day):
        if day.section_type == 'Lecture':
            return day.course.course_code + day.course.section
        else:
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
        #Use this function to append alternate reg codes?
        unique_id = self._get_id(day)
        for d, slots in list(self.weekdays.items()):
            for slot in slots:
                if slot['id'] == unique_id:
                    return True
        return False

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

    def __repr__(self):
        x = []
        od = collections.OrderedDict(sorted(self.weekdays.items()))
        for key, val in od.items():
            day = json.dumps(sorted([json.dumps(v) for v in val]))
            x.append(key + day)
        return json.dumps(x)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


def get_semester_code(d=datetime.now()):
    if d.month < 5:
        m = '01'
    elif d.month < 9:
        m = '05'
    else:
        m = '09'
    return str(d.year) + m


def get_first_sunday(semester):
    d = datetime.strptime(semester, '%Y%d')
    days_ahead = 6 - d.weekday()
    return str(d + timedelta(days_ahead))
