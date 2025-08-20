from django.contrib import admin
from .models import TaskModel, TaskReview
# Register your models here.
admin.site.register(TaskModel)
admin.site.register(TaskReview)