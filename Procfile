web: uv run manage.py runserver
celery_worker: uv run celery -A main worker -l info --pool=solo
celery_beat: uv run celery -A main beat -l info
