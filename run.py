#!env/bin/python

import os

os.environ['APP_SETTINGS']="uoit_tools.config.DevelopmentConfig"
os.environ['DATABASE_URL']="postgresql://localhost/uoit_schedule_dev"

from uoit_tools import app

if __name__=='__main__':
    app.run()

