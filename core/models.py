from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_created=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=1)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f"{self.title} {self.date_created} {self.status}"
