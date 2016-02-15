import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from uoit_tools.views import main, roomfinder, scheduler, contact

app.register_blueprint(main.main)
app.register_blueprint(roomfinder.roomfinder, url_prefix='/roomfinder')
app.register_blueprint(scheduler.scheduler, url_prefix='/scheduler')
app.register_blueprint(contact.contact, url_prefix='/contact')

