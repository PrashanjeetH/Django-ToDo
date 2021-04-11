from django.urls import path
from .views import index, mark_complete, clear_all

urlpatterns = [
    path('', index, name='home'),
    path('clear/', clear_all, name='clear'),
    path('mark/<int:pid>', mark_complete, name='completed'),
    # path('update/<int:pid>', update, name='update'),
]
