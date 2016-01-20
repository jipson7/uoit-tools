#!env/bin/python

import os

os.environ['APP_SETTINGS']="uoit_tools.config.DevelopmentConfig"
os.environ['DATABASE_URL']="postgres://fuxkqlurxyswbe:YlAF78BEc4V1gI4iTPvDW3p08J@ec2-54-225-165-132.compute-1.amazonaws.com:5432/dk2124iurbta4"

from uoit_tools import app

if __name__=='__main__':
    app.run()

