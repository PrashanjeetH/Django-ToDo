from django.contrib import admin
from .models import TodoList
# Register your models here.


@admin.register(TodoList)
class TaskAdminClass(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'status']
    list_per_page = 20
