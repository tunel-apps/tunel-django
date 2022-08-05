#!/bin/bash

# If the original migrations aren't run - do it.
# If you want to change models and run them again, you should run 
# these commands manually. The paths are hard coded for the Singularity
# container
socket=${1}
use_nginx=${2}

if [[ -z "${socket}" ]]; then
    socket=/tmp/tunel-django.sock
fi

if [[ -z "${use_nginx}" ]]; then
    use_nginx="true"
fi

# user and pass for django to create
if [[ -z "${TUNEL_USER}" ]]; then
    TUNEL_USER=tunel-user
fi
if [[ -z "${TUNEL_PASS}" ]]; then
    TUNEL_PASS=tunel-pass
fi


if [[ "${use_nginx}" == "true" ]]; then
    export TUNELDJANGO_NGINX=true
fi

printf "Socket is ${socket}\n"
if [ ! -f "migrations-run" ]; then
    sleep 3
    python3 /code/manage.py makemigrations users
    python3 /code/manage.py makemigrations main
    python3 /code/manage.py makemigrations
    python3 /code/manage.py migrate main
    python3 /code/manage.py migrate auth
    python3 /code/manage.py migrate     
    python3 /code/manage.py collectstatic --noinput
    python3 /code/manage.py add_superuser ${TUNEL_USER} ${TUNEL_PASS}
# You can uncomment this if you don't always want them to run
#    touch migrations-run
fi

if [[ "${use_nginx}" == "true" ]]; then
    /etc/init.d/nginx start
    printf "uwsgi --socket=${socket} /code/scripts/uwsgi.ini\n"
    uwsgi --socket=${socket} /code/scripts/uwsgi.ini
else
    printf "uwsgi --socket=${socket} --static-map /static=/code/static /code/scripts/uwsgi.ini\n"
    uwsgi --socket=${socket} --static-map /static=/code/static --static-map /data=/code/data /code/scripts/uwsgi-standalone.ini
fi
