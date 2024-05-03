from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path('', views.index, name='index'),
    path('privacy-policy/', views.policy, name='policy'),
    path('feedback/', views.feedback, name='feedback'),
    path('contact-us/', views.contact, name='contact'),
    path('home/', views.home, name='home'),
    path('quizes/', views.quizes, name='quizes'),
    path('quiz/', views.quiz, name='quiz'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('attempt_answer/<int:user_attempt_id>/', views.show_user_answers, name='attempt_answer'),
    path('wallet/', views.wallet, name='wallet'),
    path('withdrawal/', views.withdrawal, name='withdrawal')
]