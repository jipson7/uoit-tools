from flask import Blueprint, render_template
from uoit_tools.models import Day, Course

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home_get():
    return render_template('index.html'), 200

@main.route('/testmodel', methods=['GET'])
def test_model():
    x = Course.query.first()
    return 'ok', 200


