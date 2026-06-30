from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("account/", views.account, name="account"),
    path("account/delete_account/", views.delete_account, name="delete_account"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
]
