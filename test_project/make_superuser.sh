#!/bin/bash

#
# Create the superuser without interactive prompt.
#

username="$1"
email="$2"
password="$3"
settings="$4"

echo "from django.contrib.auth.models import User; User('$username', '$email', '$password')" | python manage.py shell --settings=$4

