#!/bin/sh
set -x


if [ "$1" = "web" ];
then

    echo "==================="
    echo "Running web"
    echo "==================="
    echo
    python manage.py migrate
    python manage.py loaddata users_seed.json
    python manage.py collectstatic --no-input
    python manage.py runserver 0.0.0.0:8000
fi