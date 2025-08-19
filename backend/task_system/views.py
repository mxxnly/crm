from django.utils import timezone
from datetime import timedelta
from .forms import TaskForm
from .models import TaskModel
from django.shortcuts import render, redirect
def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()
            return redirect('create_task')
    else:
        form = TaskForm()
    context = {
        'form': form,
    }
    return render(request, 'task_system/create_task.html', context)

def task_list_view(request):
    tasks = TaskModel.objects.all().order_by('due_date')

    now = timezone.now()
    for t in tasks:
        if t.is_completed == False and t.is_archived == False:
            if t.due_date:
                if t.due_date < now:
                    t.due_status = "overdue"
                elif t.due_date < now + timedelta(days=3):
                    t.due_status = "soon"
                else:
                    t.due_status = "ok"
            else:
                t.due_status = "no_date"

    context = {
        'tasks': tasks,
    }
    return render(request, 'task_system/task_list.html', context)

def task_complete(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    if task:
        task.is_completed = True
        task.save()
    return redirect('list_tasks')

def task_archive(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    if task:
        task.is_archived = True
        task.save()
    return redirect('list_tasks')

def task_delete(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    if task:
        task.delete()
    return redirect('list_tasks')

def task_edit(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()
            return redirect('list_tasks')
    else:
        form = TaskForm(instance=task)
    context = {
        'form': form,
        'task': task,
    }
    return render(request, 'task_system/edit_task.html', context)

def task_uncomplete(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    if task:
        task.is_completed = False
        task.save()
    return redirect('list_tasks')

def task_unarchive(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    if task:
        task.is_archived = False
        task.save()
    return redirect('list_tasks')