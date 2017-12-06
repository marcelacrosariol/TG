#!/bin/bash

service httpd stop 
python manage.py collectstatic --noinput
chmod 776 /home/toor/Documents/static_in_env/static_root/css/*
service httpd start
