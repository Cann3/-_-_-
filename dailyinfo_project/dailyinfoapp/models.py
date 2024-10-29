# dailyinfoapp/models.py

from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=50)
