from flask import Blueprint, request, jsonify
from sqlalchemy import or_, not_
from uoit_tools.models import Course, Day
from dateutil import parser as date_parser
from datetime import timedelta, datetime

roomfinder = Blueprint('roomfinder', __name__)

@roomfinder.route('/', methods=['GET'])
def find_rooms():
    date_string = request.args.get('date', None)
    try:
        d = date_parser.parse(date_string)
    except AttributeError:
        return 'Must provide valid date', 400
    day_of_week = get_day_code(d)
    t = d.time()
    semester = get_semester_code(d)
    # Add 10 minutes to start time to account for the gap in class start times
    t_offset = (datetime(100, 1, 1, t.hour, t.minute, t.second) + timedelta(minutes=10)).time()
    taken_rooms = Day.query\
                     .join(Course)\
                     .filter(Course.semester == semester)\
                     .filter(Day.day == day_of_week)\
                     .filter(t_offset > Day.start_time, t < Day.end_time)\
                     .distinct(Day.location)\
                     .with_entities(Day.location)\
                     .all()
    room_list = [x.location for x in taken_rooms]
    free_rooms = Day.query\
                    .join(Course)\
                    .filter(Course.semester == semester)\
                    .filter(not_(Day.location.in_(room_list)))\
                    .distinct(Day.location)\
                    .with_entities(Day.location)\
                    .all()
    free_room_list = create_room_json(free_rooms, t_offset, day_of_week, semester)
    return jsonify({'rooms': free_room_list}), 200

def create_room_json(free_rooms, t, day_of_week, semester):
    rooms = {}
    fail_words = ['Virtual', 'TBA', 'OFFSITE', 'Georgian'];
    for day in free_rooms:
        room = day.location
        if not any(x in room for x in fail_words):
            following = Day.query.join(Course)\
                           .filter(Course.semester == semester)\
                           .filter(Day.day == day_of_week)\
                           .filter(Day.location == room)\
                           .filter(t < Day.start_time)\
                           .order_by(Day.start_time).first()
            rooms[room] = str(following.start_time) if following else None
    return rooms

def get_semester_code(d):
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
