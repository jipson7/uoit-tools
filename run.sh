#!/bin/bash

source env/bin/activate

export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/uoit_schedule_dev

python app/__init__.py

