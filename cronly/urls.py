from django.urls import path

from . import views

app_name = "cronly"
urlpatterns = [
    path("", views.list_cronjobs, name="list_cronjobs"),
    path("new", views.new_cronjob, name="new_cronjob"),
    path("delete/<int:job_id>", views.delete_cronjob, name="delete_cronjob"),
]
