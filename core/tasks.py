from celery import shared_task
from pythonping import ping

from .models import CronJob


@shared_task
def ping_target(cronjob_id):
    job = CronJob.objects.get(id=cronjob_id)
    response = ping(job.target, count=4)
    job.avg_rtt_ms = response.rtt_avg_ms
    job.min_rtt_ms = response.rtt_min_ms
    job.max_rtt_ms = response.rtt_max_ms
    job.save()
