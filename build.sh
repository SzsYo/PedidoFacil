#!/usr/bin/env bash
# Script de construcción para Render
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "from django.db import connection; print('BASE DE DATOS:', connection.vendor, connection.settings_dict['HOST'])"