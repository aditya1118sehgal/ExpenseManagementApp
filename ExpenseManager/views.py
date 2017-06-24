from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from ExpenseManager.forms import SignUpForm, ExpenseForm
from ExpenseManager.models import Expense
from django.utils import timezone

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
