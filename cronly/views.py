import json
from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from pythonping import ping

from .forms import CronJobForm
from .models import CronJob


@login_required
def list_cronjobs(request):
    cronjobs = CronJob.objects.filter(user=request.user)
    return render(request, "cronly/list-cronjobs.html", {"cronjobs": cronjobs})

@login_required()
def new_cronjob(request):
    form = CronJobForm()
    if request.method == "POST":
        form = CronJobForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]

            host = urlparse(target).netloc
            domain = host.split(":")[0].lstrip("www.")
            response = ping(domain, count=4)

            job = CronJob.objects.create(
                user=request.user, target=domain, avg_rtt_ms=response.rtt_avg_ms,
                min_rtt_ms=response.rtt_min_ms, max_rtt_ms=response.rtt_max_ms,
                interval_seconds=form.cleaned_data.get("interval_seconds", 300),
            )

            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=job.interval_seconds,
                period=IntervalSchedule.SECONDS
            )

            PeriodicTask.objects.create(
                interval=schedule,
                name=f"ping_job_{job.id}",
                task="cronly.tasks.ping_target",
                args=json.dumps([job.id])
            )

            return redirect("cronly:list_cronjobs")

    return render(request, "cronly/new-cronjob.html", {"form": form})

def delete_cronjob(request, job_id):
    job = get_object_or_404(CronJob, id=job_id, user=request.user)
    job.delete()
    messages.success(request, "CronJob deleted successfully.")
    return redirect("cronly:list_cronjobs")
