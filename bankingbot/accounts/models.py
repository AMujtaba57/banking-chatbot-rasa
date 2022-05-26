from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
import uuid


class BankUser(models.Model):
    user = models.OneToOneField(User, related_name='user_id_account', on_delete=models.CASCADE)
    account_number = models.UUIDField(null=False, unique=True)
    full_name = models.CharField(max_length=50)
    initial_balance = models.PositiveIntegerField()
    postal_code = models.PositiveIntegerField()
    account_type = models.CharField(max_length=24)
    current_balance = models.FloatField()
    # USERNAME_FIELD = 'username'
    mobile_number = models.TextField()

    def __str__(self):
        return self.full_name 


class AccountTransactions(models.Model):
    user = models.ForeignKey(User, related_name='user_id_transactions', on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField(null=False)
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=24)

    def __str__(self):
        return f"{self.user}"