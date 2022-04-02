from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from .models import BankUser, AccountTransactions
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator

# Create your forms here.

class NewUserForm(UserCreationForm):
    initial_balance = forms.IntegerField(required=True)
    postal_code = forms.IntegerField(required=True)
    account_type = forms.ChoiceField(required=True, choices=[('C', 'Current'), ('S', 'Saving')])
    full_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password2'])

        if commit:
            user.save()
            BankUser.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                initial_balance=self.cleaned_data['initial_balance'],
                postal_code=self.cleaned_data['postal_code'],
                account_type=self.cleaned_data['account_type'],
                current_balance=float(self.cleaned_data['initial_balance']),
                account_number=uuid.uuid4()
            )
            AccountTransactions.objects.create(
                user=user,
                date_time=datetime.now(),
                amount=float(self.cleaned_data['initial_balance']),
                transaction_type="DEPOSIT",
            )
        return user


class OldUserForm(AuthenticationForm):

    numeric = RegexValidator(r'^[0-9]{4}', 'Only digit characters.')
    username = forms.CharField(required=True)
    password = forms.PasswordInput()
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class MakeTransactionForm(forms.Form):
    amount = forms.FloatField(required=True)
    transaction_type = forms.ChoiceField(required=True, choices=[('Deposit', 'Deposit'), ('Withdraw', 'Withdrawal')])
    source = forms.ChoiceField(required=True, choices=[('Web', 'Web'),('Other', 'Other')], disabled=False)

    class Meta:
        model = AccountTransactions
        fields = ("user", "datetime", "amount", "transaction_type")

    def save(self, user, commit=True):
        if commit:
            AccountTransactions.objects.create(
                user=user,
                date_time=datetime.now(),
                amount=self.cleaned_data['amount'],
                transaction_type=self.cleaned_data['transaction_type'],
            )
        return AccountTransactions
