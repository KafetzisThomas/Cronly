from django.urls import path
from . import views

app_name = "cronly"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("cronjob/new", views.new_cronjob, name="new_cronjob"),
    path("cronjob/<int:pk>/delete", views.delete_cronjob, name="delete_cronjob"),
]
