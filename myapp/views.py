from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render,redirect
from .models import Task
from .forms import TaskForm
# Create your views here.
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import *


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request,'myapp/task_list.html',{'tasks':tasks})


# @login_required
# def task_create(request):
#     if request.method=="POST":
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('task_list')
#     else:
#         form = TaskForm()
#     return render(request,'myapp/task_form.html',{'form':form})
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'myapp/task_form.html', {'form': form})


# @login_required
# def task_update(request,id):
#     task = get_object_or_404(Task,id=id)
#     if request.method == "POST":
#         form = TaskForm(request.POST,instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('task_list')
#     else:
#         form = TaskForm(instance=task)
#     return render(request,'myapp/task_form.html',{'form':form})

@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id)

    if task.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'myapp/task_form.html', {'form': form})

@login_required
def task_delete(request,pk):
    task = get_object_or_404(Task,pk=pk)
    task.delete()
    return redirect('task_list')


def register(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('task_list')
    else:
        form =UserCreationForm()
    return render(request,'myapp/register.html',{'form':form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')
