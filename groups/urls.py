from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.group_management, name='group_management'),
    path('create/', views.create_group, name='create_group'),
    path('detail/<int:group_id>/', views.group_detail, name='group_detail'),
    path('leave_group/<int:group_id>/', views.leave_group, name='leave_group'),
    path('join_group/<int:group_id>/', views.join_group, name='join_group'),
]
