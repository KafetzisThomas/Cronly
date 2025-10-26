from celery import shared_task
from django.utils import timezone
from pythonping import ping

from .models import CronJob


@shared_task
def ping_target(cronjob_id):
    job = CronJob.objects.get(id=cronjob_id)
    response = ping(job.target, count=4)

    CronJob.objects.filter(id=cronjob_id).update(
        avg_rtt_ms=response.rtt_avg_ms, min_rtt_ms=response.rtt_min_ms,
        max_rtt_ms=response.rtt_max_ms, last_pinged_at=timezone.now()
    )
