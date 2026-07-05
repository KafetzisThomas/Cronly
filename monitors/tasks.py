import json
import time
from celery import shared_task
from main.redis_client import client as redis_client
from monitors.models import Monitor
from users.utils import send_discord_service_down_alert
from .utils import track_dns_time, check_http_status

@shared_task
def check_target(monitor_id, target_url):
    dns_response = track_dns_time(target_url)
    dns_success = dns_response.get("success", False)
    ip_address = dns_response.get("ip", "Unknown")
    dns_time_ms = dns_response.get("dns_time_ms", 0.0)

    http_response = check_http_status(target_url)
    http_success = http_response.get("success", False)
    status_code = http_response.get("status_code", 0)
    response_time_ms = http_response.get("response_time_ms", 0.0)

    # overall success
    success = dns_success and http_success

    redis_key = f"monitor:{monitor_id}:checks"

    # prevent spam by checking previous status before saving new one
    previous_check_json = redis_client.lindex(redis_key, 0)
    previous_success = True
    if previous_check_json:
        previous_check = json.loads(previous_check_json)
        previous_success = previous_check.get("success", True)

    if not success and previous_success:
        try:
            monitor = Monitor.objects.get(id=monitor_id)
            send_discord_service_down_alert(monitor.user.discord_webhook_url, target_url)
        except Monitor.DoesNotExist:
            pass

    check_data = {
        "timestamp": int(time.time()),
        "ip_address": ip_address,
        "dns_time_ms": dns_time_ms,
        "http_status_code": status_code,
        "response_time_ms": response_time_ms,
        "success": success,
    }
    redis_client.lpush(redis_key, json.dumps(check_data))

    # keep only last 1000 checks, prevents memory from growing infinitely
    redis_client.ltrim(redis_key, 0, 999)
