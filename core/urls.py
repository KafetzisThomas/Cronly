from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("list_cronjobs", views.list_cronjobs, name="list_cronjobs"),
    path("new_cronjob", views.new_cronjob, name="new_cronjob"),
]
