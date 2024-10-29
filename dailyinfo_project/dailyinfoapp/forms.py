# dailyinfoapp/forms.py

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
