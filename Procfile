web: python manage.py runserver
worker: celery -A trends worker --loglevel=info
beat: celery -A trends beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
