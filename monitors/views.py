import json
from datetime import datetime
from urllib.parse import urlparse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from main.redis_client import client as redis_client
from .models import Monitor
from .forms import MonitorForm

@login_required
def dashboard(request):
    monitors = Monitor.objects.filter(user=request.user)

    for job in monitors:
        redis_key = f"monitor:{job.id}:pings"

        latest_ping_json = redis_client.lindex(redis_key, 0)
        if latest_ping_json:
            latest_ping = json.loads(latest_ping_json)

            job.current_avg = latest_ping.get("avg_rtt_ms")
            job.current_min = latest_ping.get("min_rtt_ms")
            job.current_max = latest_ping.get("max_rtt_ms")
            job.status = "Up" if latest_ping.get("success") else "Down"

            # convert unix timestamp to readable format
            timestamp = latest_ping.get("timestamp")
            if timestamp:
                job.current_last_checked = datetime.fromtimestamp(timestamp)
        else:
            job.current_avg = "Pending"
            job.current_min = "Pending"
            job.current_max = "Pending"
            job.status = "Pending"
            job.current_last_checked = None

    return render(request, "monitors/dashboard.html", {"monitors": monitors})

@login_required
def new_monitor(request):
    if request.method == "POST":
        form = MonitorForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]
            host = urlparse(target).netloc
            domain = host.split(":")[0].lstrip("www.")

            job = Monitor.objects.create(
                target=domain,
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
                task="monitors.tasks.ping_target",
                args=json.dumps([job.id, domain])
            )
            return redirect("monitors:dashboard")
    else:
        form = MonitorForm()

    return render(request, "monitors/new_monitor.html", {"form": form})

@login_required
def delete_monitor(request, pk):
    job = get_object_or_404(Monitor, id=pk, user=request.user)

    PeriodicTask.objects.filter(name=f"ping_job_{job.id}").delete()

    redis_key = f"monitor:{job.id}:pings"
    redis_client.delete(redis_key)

    job.delete()

    messages.success(request, "Monitor deleted successfully.")
    return redirect("monitors:dashboard")
