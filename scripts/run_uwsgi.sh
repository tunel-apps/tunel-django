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

# Derive api socket from main sock
socket_dir=$(dirname "${socket}")
api_socket=${socket_dir}/api.sock

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
printf "API socket is ${api_socket}\n"

if [ ! -f "migrations-run" ]; then
    sleep 3
    python3 /code/manage.py makemigrations admin
    python3 /code/manage.py makemigrations users
    python3 /code/manage.py makemigrations main
    python3 /code/manage.py makemigrations
    python3 /code/manage.py migrate users
    python3 /code/manage.py migrate admin
    python3 /code/manage.py migrate main
    python3 /code/manage.py migrate auth
    python3 /code/manage.py migrate      
    python3 /code/manage.py collectstatic --noinput
    python3 /code/manage.py add_superuser ${TUNEL_USER} ${TUNEL_PASS}
    touch migrations-run
fi

if [[ "${use_nginx}" == "true" ]]; then
    echo "Starting application using nginx..."
    /etc/init.d/nginx start
    printf "uwsgi --socket=${socket} /code/scripts/uwsgi.ini\n"
    uwsgi --socket=${socket} /code/scripts/uwsgi.ini &
    echo "Return value main server: $?"
    printf "uwsgi --wsgi-file tuneldjango/wsgi.py --master --socket ${api_socket} --http-socket ${api_socket}\n"
    uwsgi --chdir /code --wsgi-file tuneldjango/wsgi.py --master --socket ${api_socket} --http-socket ${api_socket}
    echo "Return value api server: $?"
else
    echo "Starting application without using nginx..."
    # This could better be run with the emperor, but we need to be able to provide sockets as envars/variables
    printf "uwsgi --http-socket=${socket} --socket=${socket} --static-map /static=/code/static --static-map /data=/code/data /code/scripts/uwsgi-standalone.ini\n"
    uwsgi --http-socket=${socket} --socket=${socket} --static-map /static=/code/static --static-map /data=/code/data /code/scripts/uwsgi-standalone.ini &
    echo "Return value main server: $?"
    printf "uwsgi --wsgi-file tuneldjango/wsgi.py --master --socket ${api_socket} --http-socket ${api_socket}\n"
    uwsgi --chdir /code --wsgi-file tuneldjango/wsgi.py --master --socket ${api_socket} --http-socket ${api_socket}
    echo "Return value api server: $?"
fi
