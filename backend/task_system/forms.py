from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import TaskModel
from authentication.models import CustomUser

class TaskForm(forms.ModelForm):
    priority = forms.IntegerField(
        label="Priority (1–5 stars)",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 5,
            'placeholder': 'Enter priority (1-5)'
        })
    )

    due_date = forms.DateTimeField(
        label="Due Date",
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',  
            'class': 'form-control'
        })
    )

    title = forms.CharField(
        label="Task Title",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task title', 'rows': 1})
    )

    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task description', 'rows': 4})
    )

    for_who = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        label="Assign to",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TaskModel
        fields = ['title', 'description', 'due_date', 'priority', 'for_who']
