import json
from pythonping import ping
from urllib.parse import urlparse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import CronJob
from .forms import CronJobForm

@login_required
def dashboard(request):
    cronjobs = CronJob.objects.filter(user=request.user)
    return render(request, "cronly/dashboard.html", {"cronjobs": cronjobs})

@login_required
def new_cronjob(request):
    if request.method == "POST":
        form = CronJobForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]
            host = urlparse(target).netloc
            domain = host.split(":")[0].lstrip("www.")
            response = ping(domain, count=4)

            job = CronJob.objects.create(
                target=domain,
                avg_rtt_ms=response.rtt_avg_ms,
                min_rtt_ms=response.rtt_min_ms,
                max_rtt_ms=response.rtt_max_ms,
                interval_seconds=form.cleaned_data.get("interval_seconds", 300),
                user=request.user,
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
            return redirect("cronly:dashboard")
    else:
        form = CronJobForm()

    return render(request, "cronly/new_cronjob.html", {"form": form})

@login_required
def delete_cronjob(request, job_id):
    job = get_object_or_404(CronJob, id=job_id, user=request.user)
    job.delete()
    messages.success(request, "Cronjob deleted successfully.")
    return redirect("cronly:dashboard")
