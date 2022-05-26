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
    path("", views.user_login, name="user_login"),
    path("verify/", views.verify, name="verify"),
    path("deposit_verification/", views.deposit_verification, name="deposit_verification"),
    path("post_deposit_verification/", views.post_deposit_verification, name="post_deposit_verification"),
    path("withdraw_verification/", views.withdraw_verification, name="withdraw_verification"),
    path("post_withdraw_verification/", views.post_withdraw_verification, name="post_withdraw_verification"),
    path("money_transfer/", views.money_transfer, name="money_transfer"),
    path("post_money_transfer/", views.post_money_transfer, name="post_money_transfer"),
    # path("transfer_verification/", views.transfer_verification, name="transfer_verification"),


]