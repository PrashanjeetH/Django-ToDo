from pkgutil import ImpImporter
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import TodoList
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
# Create your views here.


@login_required
def index(request):
    # print(request.user.username)
    completed = TodoList.objects.filter(user=request.user.id)
    context = {
        'title': 'Home',
        'heading': "Your ToDo's ",
        'completed_tasks': completed.filter(status=1).order_by('-id')[:5],
        'submit': 'Add',
    }
    if request.method == 'POST' and request.POST.get('title') != '':
        entry = TodoList(user=request.user,
                         title=request.POST.get('title'),
                         date_created=datetime.now(),
                        #  date_created=make_aware(datetime.now())  # To handle Naive date time warning
                         status=0)
        entry.save()
        tasks = TodoList.objects.filter(user=request.user.id).order_by('-id')
        context['entries'] = tasks.filter(status=0)[:10]
        return render(request, 'core/base.html', context)
    else:
        tasks = TodoList.objects.filter(user=request.user.id)
        context['entries'] = tasks.filter(status=0)
        return render(request, 'core/base.html', context)


@login_required
def mark_complete(request, pid):
    if request.method == 'GET':
        entry = TodoList.objects.get(pk=pid)
        entry.status = 1
        entry.date_completed = datetime.now()
        entry.save()
    return redirect('home')

@login_required
def update(request, pid):
    if request.method == 'GET':
        # Get 10 latest tasks to show
        completed = TodoList.objects.filter(status=1).order_by('-id')[:10]
        tasks = TodoList.objects.filter(status=0)
        context = {
            'title': 'Update',
            'heading': 'Update your task',
            'completed_tasks': completed,
            'entries': tasks,
            'submit': 'Update',
        }

        entry = TodoList.objects.get(pk=pid)
        context['value'] = entry.title
        entry.delete()
        return render(request, 'core/base.html', context)
    elif request.method =='POST':
        return index(request)
    else:
        return redirect('home')


def clear_all(request):
    entries = TodoList.objects.filter(user=request.user.id).filter(status=1)
    entries.delete()
    return redirect('home')