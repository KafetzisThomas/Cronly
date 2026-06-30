import requests
from django.conf import settings
from datetime import datetime

def send_discord_service_down_alert(webhook_url, monitor):
    if settings.DEBUG or not webhook_url:
        return

    payload = {
        "username": "Cronly Alerts",
        "embeds": [{
            "title": "🚨 Service is DOWN",
            "color": 15158332,
            "fields": [
                {"name": "Service", "value": f"`{monitor}`", "inline": True},
                {"name": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True},
                {"name": "Status", "value": "🔴 Offline", "inline": True},
            ]
        }]
    }

    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except requests.exceptions.RequestException:
        pass  # ignore network errors to prevent celery from crashing
