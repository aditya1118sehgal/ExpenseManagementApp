from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ExpenseManager.models import Expense
import datetime

class SignUpForm(UserCreationForm):
    role = forms.CharField(help_text='A=admin, R=regular')

    class Meta:
        model = User
        fields = ('username', 'role', 'password1', 'password2', )

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = ('title', 'text', 'amount')

class ReportForm(forms.Form):
    start = forms.DateTimeField(initial=datetime.date.today)
    end = forms.DateTimeField(initial=datetime.date.today)
