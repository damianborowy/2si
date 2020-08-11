from django.shortcuts import render

from factory.models import Rule, Employee, Location, Category


def index(request):
    return render(request, "factory/index.html", {})


def select_worker(request, positive, action_type):
    workers = Employee.objects.all()

    return render(request, "factory/select_worker.html",
                  {"action_type": action_type, "workers": workers, "positive": positive})


def select_location(request, positive, worker_id):
    locations = Location.objects.all()

    return render(request, "factory/select_location.html",
                  {"worker_id": worker_id, "positive": positive, "locations": locations})


def contribute_bos(request, positive, worker_id, location_id):
    categories = Category.objects.filter(type="B")

    return render(request, "factory/contribute_bos.html",
                  {"positive": positive, "worker_id": worker_id, "location_id": location_id, "categories": categories})


def contribute_quos(request, positive, worker_id):
    categories = Category.objects.filter(type="Q")
    print(categories.rule_set.all())

    return render(request, "factory/contribute_quos.html",
                  {"positive": positive, "worker_id": worker_id, "categories": categories})


def stats(request):
    return render(request, "factory/stats.html")
