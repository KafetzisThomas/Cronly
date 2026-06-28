import redis
from django.conf import settings

client = redis.from_url(settings.REDIS_DATA_URL, decode_responses=True)
