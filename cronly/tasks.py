import json
import time
from celery import shared_task
from pythonping import ping
from main.redis_client import client as redis_client

@shared_task
def ping_target(monitor_id, target_url):
    """
    Ping target and store results in redis.
    """
    response = ping(target_url, count=4)

    # timeseries data point
    ping_data = {
        "timestamp": int(time.time()),
        "avg_rtt_ms": response.rtt_avg_ms,
        "min_rtt_ms": response.rtt_min_ms,
        "max_rtt_ms": response.rtt_max_ms,
        "success": response.success(),
    }
    redis_key = f"monitor:{monitor_id}:pings"
    redis_client.lpush(redis_key, json.dumps(ping_data))

    # keep only last 1000 pings, prevents memory from growing infinitely
    redis_client.ltrim(redis_key, 0, 999)
