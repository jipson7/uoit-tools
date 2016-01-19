#!/bin/bash

source env/bin/activate

export APP_SETTINGS="config.DevelopmentConfig"

python app/__init__.py

