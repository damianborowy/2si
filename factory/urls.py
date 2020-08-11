from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("worker/<int:positive>/<str:action_type>/", views.select_worker, name="select_worker"),
    path("location/<int:positive>/<int:worker_id>/", views.select_location, name="select_location"),
    path("contribute/<int:positive>/<int:worker_id>/<int:location_id>/", views.contribute_bos, name="contribute_bos"),
    path("contribute/<int:positive>/<int:worker_id>/", views.contribute_quos, name="contribute_quos"),
    path("stats/", views.stats, name="stats"),
]
