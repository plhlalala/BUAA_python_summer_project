from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.question_management, name='question_management'),
    path('share_question/<int:question_id>/', views.share_question, name='share_question'),
    path('create/', views.create_question, name='create_question'),
    path('detail/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ocr_image/', views.ocr_image, name='ocr_image'),
    path('create_set/', views.create_question_set, name='create_question_set'),
    path('set_detail/<int:question_set_id>/', views.question_set_detail, name='question_set_detail'),
    path('add_question_to_set/<int:question_set_id>/', views.add_question_to_set, name='add_question_to_set'),
    path('remove_question_from_set/<int:question_set_id>/<int:question_id>/', views.remove_question_from_set,
         name='remove_question_from_set'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('share_question_set/<int:question_set_id>/', views.share_question_set, name='share_question_set'),
]
