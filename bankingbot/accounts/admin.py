from django.contrib import admin
from .models import BankUser,AccountTransactions

admin.site.register(BankUser)
admin.site.register(AccountTransactions)

