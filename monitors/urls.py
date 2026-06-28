from django.urls import path
from . import views

app_name = "monitors"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("monitors/create", views.new_monitor, name="new_monitor"),
    path("monitors/<int:pk>/delete", views.delete_monitor, name="delete_monitor"),
]
