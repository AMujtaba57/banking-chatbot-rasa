from django.urls import path
from . import views

app_name = "accounts"


urlpatterns = [
    path("register/", views.user_registration, name="user_registration"),
    path("login/", views.user_login, name="user_login"),
    path("history/", views.history_transaction, name="history_transaction"),
    path("logout/", views.user_logout, name="user_logout"),
    path("make-transaction/", views.user_transaction, name="user_transaction"),
    path("api/user-profile", views.user_profile, name="user_profile"),
    path("home/", views.home, name="home"),
    path("", views.user_login, name="user_login")

]