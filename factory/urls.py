from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("contribute/<str:action_type>/", views.select_worker),
    path("contribute/<str:action_type>/<int:worker_id>", views.contribute),
    path("stats/", views.stats)
]
