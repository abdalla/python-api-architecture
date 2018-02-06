#!/usr/bin/env bash

export FLASK_APP=app/__init__.py
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

flask db init
flask db migrate
flask db upgrade
#flask db --help