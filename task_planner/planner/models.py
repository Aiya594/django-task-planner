from django.db import models
from django.conf import settings

# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="projects")
    title =models.CharField(max_length=255) 
    description=models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "Todo"
        IN_PROGRESS = "in_progress", "In progress"
        DONE = "done", "Done"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name="tasks")
    title=models.CharField(max_length=255)
    description=models.TextField(blank=True)

    status=models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.TODO)
    priority=models.CharField(
        max_length=20, 
        choices=Priority.choices, 
        default=Priority.MEDIUM)

    deadline =models.DateField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name="comments")
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="comments")
    text =models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
