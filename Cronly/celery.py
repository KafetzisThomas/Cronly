import os

from celery import Celery

# Set the default django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cronly.settings')

app = Celery('Cronly')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# This allows periodic tasks to be managed dynamically via the database,
# so tasks can be created, updated or removed without changing code or restarting Celery Beat.
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# start redis: sudo service redis-server start
# check if it's running, should be "PONG": redis-cli ping
# run django server: uv run manage.py runserver
# open 2 extra terminals and run:
# terminal 1: celery -A Cronly worker -l info --pool=solo
# terminal 2: celery -A Cronly beat -l info
