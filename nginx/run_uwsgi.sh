#!/bin/bash

# If the original migrations aren't run - do it.
# If you want to change models and run them again, you should run 
# these commands manually.
if [ ! -f "migrations-run" ]; then
    sleep 3
    python3 manage.py makemigrations main
    python3 manage.py makemigrations
    python3 manage.py migrate main
    python3 manage.py migrate auth
    python3 manage.py migrate 
    python3 manage.py collectstatic --noinput
#    touch migrations-run
fi

/etc/init.d/nginx start
uwsgi nginx/uwsgi.ini
