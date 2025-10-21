from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("register/", views.register, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
