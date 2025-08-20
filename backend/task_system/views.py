from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from authentication.models import CustomUser
from .forms import TaskForm, TaskReviewFormUpdate
from .models import TaskModel, TaskReview
from django.shortcuts import get_object_or_404, render, redirect
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

def review_page(request):
    reviews = TaskReview.objects.all().select_related('task', 'submitted_by')

    # Фільтруємо по статусу
    status = request.GET.get('status')
    if status in ['pending', 'approved', 'rejected']:
        reviews = reviews.filter(status=status)

    # Фільтруємо по користувачу, який відправив на рев’ю
    submitted_by = request.GET.get('submitted_by')
    if submitted_by and submitted_by.isdigit():
        reviews = reviews.filter(submitted_by_id=int(submitted_by))

    # Фільтруємо по користувачу, який робив рев’ю
    reviewed_by = request.GET.get('reviewed_by')
    if reviewed_by and reviewed_by.isdigit():
        reviews = reviews.filter(reviewed_by_id=int(reviewed_by))

    # Список всіх користувачів для select-полів
    users = CustomUser.objects.all()

    context = {
        'tasks_review': reviews.order_by('-send_to_review'),
        'users': users,
    }
    return render(request, 'task_system/review_page.html', context)

def edit_review(request, review_id):
    review = get_object_or_404(TaskReview, id=review_id)

    if request.method == 'POST':
        form = TaskReviewFormUpdate(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('/review-page')
    else:
        form = TaskReviewFormUpdate(instance=review)  

    if request.GET.get('modal') == '1':
        from django.template.loader import render_to_string
        html = render_to_string('edit_review_modal.html', {'form': form})
        return HttpResponse(html)

    return render(request, 'edit_review_page.html', {'form': form, 'review': review})
