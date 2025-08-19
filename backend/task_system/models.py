from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TaskModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by= models.ForeignKey(
        'authentication.CustomUser',
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    due_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    priority = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    for_who = models.ManyToManyField('authentication.CustomUser', related_name='tasks')

    def __str__(self):
        return "Task {}. Priority: {} stars. To be completed by {}".format(self.title, self.priority, self.due_date)
