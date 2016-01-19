from flask import Blueprint
from uoit_tools.models import Course, Day

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home_get():
    return 'Hello World from Blueprint', 200
