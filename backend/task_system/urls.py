from django.urls import path, include
from . import views
urlpatterns = [
    path('create-task/', views.create_task_view, name='create_task'),
    path('list-tasks/', views.task_list_view, name='list_tasks'),
    path('complete-task/<int:task_id>/', views.task_complete, name='complete_task'),
    path('archive-task/<int:task_id>/', views.task_archive, name='archive_task'),
    path('delete-task/<int:task_id>/', views.task_delete, name='delete_task'),
    path('edit-task/<int:task_id>/', views.task_edit, name='edit_task'),
    path('unarchive-task/<int:task_id>/', views.task_unarchive, name='unarchive_task'),
    path('uncomplete-task/<int:task_id>/', views.task_uncomplete, name='uncomplete_task'),
    path('review-page/', views.review_page, name='review_page'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),

]