from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("new_cronjob", views.new_cronjob, name="new_cronjob"),
]
