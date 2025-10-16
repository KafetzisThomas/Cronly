import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pythonping import ping

from .models import CronJob


@csrf_exempt  # TODO: Remove this when will use forms, now disabled for postman testing
def new_cronjob(request):
    if request.method == "POST":
        body = json.loads(request.body)
        target = body.get("target")

        if not target:
            return JsonResponse({"error": "No target provided"}, status=400)

        response = ping(target, count=4)

        job = CronJob.objects.create(
            target=target, avg_rtt_ms=response.rtt_avg_ms,
            min_rtt_ms=response.rtt_min_ms,max_rtt_ms=response.rtt_max_ms,
        )

        return JsonResponse({
            "id": job.id, "target": job.target, "avg_rtt_ms": job.avg_rtt_ms,
            "min_rtt_ms": job.min_rtt_ms, "max_rtt_ms": job.max_rtt_ms, "created_at": job.created_at,
        })

    else:
        return JsonResponse({"error": "POST request required"}, status=405)
