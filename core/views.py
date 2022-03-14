from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import TodoList
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
    # print(request.user.username)
    completed = TodoList.objects.filter(user=request.user.id)
    context = {
        'title': 'Home',
        'heading': "Your ToDo's ",
        'completed_tasks': completed.filter(status=1).order_by('-id')[:5],
    }
    if request.method == 'POST' and request.POST.get('title') != '':
        entry = TodoList(user=request.user,
                         title=request.POST.get('title'),
                         date_created=datetime.now(),
                         status=0)
        entry.save()
        tasks = TodoList.objects.filter(user=request.user.id)
        context['entries'] = tasks.filter(status=0)
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


# def update(request, pid):
#     if request.method == 'GET':
#         completed = TodoList.objects.filter(status=1).order_by('-id')[:10]
#         tasks = TodoList.objects.filter(status=0)
#         context = {
#             'title': 'Home',
#             'heading': 'Heading',
#             'completed_tasks': completed,
#             'entries': tasks,
#         }
#         entry = TodoList.objects.get(pk=pid)
#         context['value'] = entry.title
#         return render(request, 'core/base.html', context)
#     else:
#         return redirect('home')


def clear_all(request):
    entries = TodoList.objects.filter(user=request.user.id)
    entries.delete()
    return redirect('home')