release: python manage.py makemigration && python manage.py migrate

web: gunicorn aduj_visuals.wsgi:application