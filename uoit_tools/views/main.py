from flask import Blueprint, render_template
from uoit_tools.models import Course, Day

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home_get():
    return render_template('index.html'), 200


@main.route('/dbtest', methods=['GET'])
def test_get():
    test_course = Course.query.filter_by(code='3010U').first()
    print(dir(test_course))
    return test_course.code, 200

