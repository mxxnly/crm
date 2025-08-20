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


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TaskReview(models.Model):
    task = models.ForeignKey(
        'task_system.TaskModel',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    submitted_by = models.ForeignKey(
        'authentication.CustomUser',
        on_delete=models.CASCADE,
        related_name='submitted_reviews'
    )
    reviewed_by = models.ForeignKey(
        'authentication.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='task_reviews'
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    send_to_review = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    files = models.FileField(upload_to='task_reviews/', null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Review for {self.task.title} by {self.submitted_by.username} [{self.status}]"
