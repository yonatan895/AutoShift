from django.urls import path

from . import views

urlpatterns = [
    path("run/", views.run_automation, name="run_automation"),
]
