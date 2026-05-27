from django.shortcuts import render, redirect
from .models import *
from django import forms
from django.contrib import messages
from django.forms import inlineformset_factory
from .filter import DayRangeFilter
from django.contrib.auth.decorators import login_required

# Login imports
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, StepForm


def register_page(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login_page')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login_page')
def home(request):
    user_ = User.objects.get(id=request.user.id)
    days = DaySteps.objects.filter(user=user_)
    total_days = days.count()
    total_steps = 0

    myFilter = DayRangeFilter(request.GET, queryset=days)
    days = myFilter.qs

    for day in days:
        total_steps += day.steps_counter

    context = {'myFilter': myFilter, 'days': days, 'total_days': total_days,
               'total_steps': total_steps}
    return render(request, 'dashboard.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
def add_steps(request, pk):
    user = User.objects.get(id=pk)
    StepForm = inlineformset_factory(
        User, DaySteps, widgets={
            'steps_counter': forms.TextInput(attrs={'style': 'text-align:center;'}),
            'day': forms.TextInput(attrs={'style': 'text-align:center;'})}, fields=('steps_counter', 'day'), max_num=1, can_delete=False)
    formset = StepForm(
        queryset=DaySteps.objects.none(), instance=user)
    if request.method == 'POST':
        formset = StepForm(request.POST, instance=user)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {'formset': formset}
    return render(request, 'add_steps.html', context)
