from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from ExpenseManager.forms import SignUpForm, ExpenseForm, ReportForm
from ExpenseManager.models import Expense
from django.utils import timezone
from datetime import datetime

@login_required
def home(request):
    expenses = Expense.objects.all()
    user_is_admin = request.user.profile.is_admin()
    if user_is_admin:
        expenses = Expense.objects.all()
    else:
        expenses = Expense.objects.filter(author=request.user)
    return render(request, 'home.html',{'expenses':expenses} )

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.role = form.cleaned_data.get('role')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    return render(request, 'login.html')

# CRUD expenses:

# create expense
def expense_new(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('expense_detail', pk=post.pk)
    else:
        form = ExpenseForm()
    return render(request, 'expense_edit.html', {'form': form})

# read expense
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'expense_detail.html', {'expense': expense})

# update expense
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.author = request.user
            expense.published_date = timezone.now()
            expense.save()
            return redirect('expense_detail', pk=expense.pk)
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense_edit.html', {'form': form})

# delete expense
def expense_delete(request, pk):
    Expense.objects.filter(id=pk).delete()
    return redirect('home')

# expense report
def report(request):
    form = ReportForm()
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            start_str=request.POST.get('start')
            end_str=request.POST.get('end')
            start_time=datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
            end_time=datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
            expenses = get_user_expenses(request.user, start_time, end_time)
            total = compute_total(expenses)
            return render(request,'report.html', {'expenses':expenses, 'total':total})
    else:
        form = ReportForm()
    return render(request, 'generate_report.html', {'form': form})

# helper methods for generating an expense report

# returns list of expenses for a specified user from a start datetime to end datetime
def get_user_expenses(user, start, end):
    all_expenses = Expense.objects.filter(author=user)
    expenses=[]
    for expense in all_expenses:
        print(expense.created_date)
        if expense.created_date.replace(tzinfo=None) > start and expense.created_date.replace(tzinfo=None) < end:
            expenses = expenses + [expense]
    return expenses
# computes the total from a list of expenses
def compute_total(expenses):
    total = 0
    for expense in expenses:
        total = total + expense.amount
    return total
