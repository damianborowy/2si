from django.shortcuts import render, redirect

from factory.models import Rule, Employee, Location, Category, Contribution, ContributionRule, Settings


def save_contribution(request, positive, worker_id, location_id=None):
    employee = Employee.objects.get(id=worker_id)
    location = Location.objects.get(id=location_id) if location_id is not None else None
    contribution = Contribution(employee=employee, location=location)
    contribution.save()

    for rule_id in request.POST.getlist("rule"):
        rule = Rule.objects.get(id=rule_id)
        feedback_type = "P" if positive == 1 else "C"
        contribution_rule = ContributionRule(contribution=contribution, rule=rule, feedback_type=feedback_type)
        contribution_rule.save()


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
    if request.method == "POST":
        save_contribution(request, positive, worker_id, location_id)

        return redirect(to="thanks")
    else:
        categories = Category.objects.filter(type="B")
        max_selections = Settings.objects.all()[0].max_selections

        return render(request, "factory/contribute.html",
                      {"positive": positive, "worker_id": worker_id, "location_id": location_id,
                       "categories": categories, "action_type": "B", "max_selections": max_selections})


def contribute_quos(request, positive, worker_id):
    if request.method == "POST":
        save_contribution(request, positive, worker_id)

        return redirect(to="thanks")
    else:
        categories = Category.objects.filter(type="Q")
        max_selections = Settings.objects.all()[0].max_selections

        return render(request, "factory/contribute.html",
                      {"positive": positive, "worker_id": worker_id,
                       "categories": categories, "action_type": "Q", "max_selections": max_selections})


def thanks(request):
    return render(request, "factory/thanks.html")


def stats(request):
    return render(request, "factory/stats.html")
