from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home_get():
    return 'Hello World from Blueprint', 200
