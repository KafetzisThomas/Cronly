import json
import time
from celery import shared_task
from pythonping import ping
from main.redis_client import client as redis_client
from monitors.models import Monitor
from users.utils import send_discord_service_down_alert

@shared_task
def ping_target(monitor_id, target_url):
    """
    Ping target and store results in redis.
    """
    try:
        response = ping(target_url, count=4)
        success = response.success()
        avg_rtt = response.rtt_avg_ms
        min_rtt = response.rtt_min_ms
        max_rtt = response.rtt_max_ms
    except Exception:
        success = False
        avg_rtt = 0.0
        min_rtt = 0.0
        max_rtt = 0.0

    redis_key = f"monitor:{monitor_id}:pings"

    # prevent spam by checking previous ping status before saving new one
    previous_ping_json = redis_client.lindex(redis_key, 0)
    previous_success = True
    if previous_ping_json:
        previous_ping = json.loads(previous_ping_json)
        previous_success = previous_ping.get("success", True)

    if not success and previous_success:
        try:
            monitor = Monitor.objects.get(id=monitor_id)
            send_discord_service_down_alert(monitor.user.discord_webhook_url, target_url)
        except Monitor.DoesNotExist:
            pass

    ping_data = {
        "timestamp": int(time.time()),
        "avg_rtt_ms": avg_rtt,
        "min_rtt_ms": min_rtt,
        "max_rtt_ms": max_rtt,
        "success": success,
    }
    redis_client.lpush(redis_key, json.dumps(ping_data))

    # keep only last 1000 pings, prevents memory from growing infinitely
    redis_client.ltrim(redis_key, 0, 999)
