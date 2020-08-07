from django.shortcuts import render

from factory.models import Rule


def index(request):
    return render(request, "factory/index.html", {})


def select_worker(request, action_type):
    return render(request, "factory/select_worker.html", {"action_type": action_type})


def contribute(request, action_type, worker_id):
    return render(request, "factory/contribute.html", {"action_type": action_type, "worker_id": worker_id})


def stats(request):
    return render(request, "factory/stats.html")
