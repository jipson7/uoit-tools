from flask import Blueprint, request, jsonify
from sqlalchemy import or_, not_
from uoit_tools.models import Course, Day
from dateutil import parser as date_parser
from datetime import timedelta, datetime

scheduler = Blueprint('scheduler', __name__)

@scheduler.route('/', methods=['GET'])
def create_schedules():
    return 'OK', 200

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
