#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Make migrations
echo "Make migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create Django admin superuser or update password
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
auth_user = get_user_model()
if auth_user.objects.filter(username='${DJANGO_SUPERUSER_NAME}').exists():
    user = auth_user.objects.get(username='${DJANGO_SUPERUSER_NAME}')
    user.set_password('${DJANGO_SUPERUSER_PASSWORD}')
    user.save()
else:
    auth_user.objects.create_superuser('${DJANGO_SUPERUSER_NAME}', '', '${DJANGO_SUPERUSER_PASSWORD}')
EOF

exec "$@"
