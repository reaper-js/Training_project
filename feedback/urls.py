
from django.urls import path
from .views import create_question, answer_question, teacher_dashboard,home



urlpatterns = [
    path('create_question/', create_question, name='create_question'),
    path('answer_question/<int:question_id>/', answer_question, name='answer_question'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
    # path('send_otp/', teacher_dashboard, name='send_otp'),
    # path('verify_otp/', teacher_dashboard, name='verify_otp'),
    path('home',home,name='learner_trainer_home'),
]
