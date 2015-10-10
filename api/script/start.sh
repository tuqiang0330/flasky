#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh

deactivate
workon flasky

export FLASKY_API_CONFIG=/home/flasky/api/script/config.py

nohup mod_wsgi-express start-server /home/flasky/api/script/index.wsgi --port=10080 --reload-on-changes --server-root=/home/flasky/api/apache >/dev/null 2>&1 &
