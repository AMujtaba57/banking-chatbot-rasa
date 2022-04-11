from email import message
from django.shortcuts import render, redirect
import django_tables2 as tables
from .forms import NewUserForm, OldUserForm, MakeTransactionForm, AccountTransactions, BankUser
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages  # import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time, json
import email.message
import smtplib
import random


def home(request):
    if request.user.is_authenticated:
        return render(request=request, template_name="welcome.html")

    return redirect('/login')

def user_registration(request):
    msg = ""
    if request.user.is_authenticated:
        return redirect('/history')

    if request.method == "POST":
        
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            time.sleep(1)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/login")
        else:
            msg = form.errors
    form = NewUserForm
    return render(request=request, template_name="registration.html", context={"registration_form": form, "msg":msg})


class AccountTransactionsTable(tables.Table):
    class Meta:
        model = AccountTransactions


def history_transaction(request):
    if request.user.is_authenticated:
        table = AccountTransactionsTable(AccountTransactions.objects.all().filter(user=request.user))
        profile = BankUser.objects.get(user=request.user)

        return render(request=request, template_name="transactionhistory.html",
                      context={"t_list": table, 'profile': {'name': profile.full_name
                          , 'a_no': profile.account_number
                          , 'current': profile.current_balance}})
    return redirect('/login')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request=request, template_name="logout.html")

    form = OldUserForm
    return render(request=request, template_name="login.html", context={"login_form": form})


def chatbot_page(request):
    if request.user.is_authenticated:
        return render(request=request, template_name="chatbot.html")
    else:
        return redirect('/login')

def verify(request):
    login_msg = "Not Authenticated user"
    if request.user.is_authenticated:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        msg = email.message.Message()
        msg['Subject'] = 'Chatbot Verified Link'
        msg['From'] = 'Verification email'
        msg['To'] = request.user.email
        msg.add_header('Content-Type','text/html')
        msg.set_payload("""
        This is the verified message from Rasa-ChatBot for Authorized status. Click the below link 
        to visit your account.<br>
        http://127.0.0.1:8000/home/.
        This message is from CHATBOT-RASA powered by Musa.<br>
        For more Information contact at abc@gmail.com
        """)
        s.login("", "")
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()

        login_msg = """
            This message is only for registered user.
            Varification Email sent to your register email account. 
        """
    return render(request=request, template_name="verify.html", context={"login_msg": login_msg})

def user_login(request):
    msg = ""
    if request.user.is_authenticated:
        return redirect('/verify')

    if request.method == "POST":
        
        form = OldUserForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/verify')
            else:
               msg = form.errors
            messages.success(request, "Registration successful.")
            return redirect("/login")
        msg = form.errors

    form = OldUserForm
    return render(request=request, template_name="login.html", context={"login_form": form, "msg":msg})


def user_transaction(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = MakeTransactionForm(data=request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                transaction_type = form.cleaned_data['transaction_type']
                source = form.cleaned_data['source']

                b_user = BankUser.objects.get(user=request.user)
                if transaction_type == 'Withdraw':
                    if b_user.current_balance >= amount:
                        b_user.current_balance = b_user.current_balance - amount
                        b_user.save()
                        form.save(user=request.user)
                        if source == 'Other':
                            rand_nmbr = random.randint(1000, 9999)
                            return JsonResponse(json.dumps({'Status': 1, 'Message': f'Amount can be Withdrawn from any nearest bank/atm using this `{rand_nmbr}` otp'}), safe=False)
                        else:
                            return redirect("/history")
                    else:
                        messages.error(request, "Not Enough Money")
                        if source == 'Other':
                            return JsonResponse(json.dumps({'Status': 0, 'Message': 'Not Enough Money'}), safe=False)
                        else:
                            return redirect("/history")
                elif transaction_type == 'Deposit':
                    b_user.current_balance = b_user.current_balance + amount
                    b_user.save()

                    form.save(user=request.user)
                    if source == 'Other':
                        rand_nmbr = random.randint(1000, 9999)
                        return JsonResponse(json.dumps({'Status': 1, 'Message': f'Amount can be Deposit using this `{rand_nmbr}` otp in any nearest bank/atm'}), safe=False)
                    else:
                        return redirect("/history")

                messages.error(request, form.data)

            messages.error(request, form.errors)
        form = MakeTransactionForm
        return render(request=request, template_name="maketransaction.html", context={"MakeTransaction_form": form})
    else:
        return redirect("/login")


def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            profile = BankUser.objects.get(user=request.user)
            return JsonResponse(json.dumps(
                {'profile': {'name': profile.full_name, 'a_no': str(profile.account_number), 'a_type': profile.account_type,
                             'current': profile.current_balance}}), safe=False)

    return redirect('/login')
