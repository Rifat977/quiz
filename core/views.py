from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from course.models import QuestionPattern, UserAttempt

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    user = request.user
    user_course = request.user.course

    f_quizzes = QuestionPattern.objects.filter(subject__course=user_course, is_featured=True).select_related('subject__course').all()
    f_participation_status = {}



    for quiz in f_quizzes:
        attempt = UserAttempt.objects.filter(user=user, question__pattern=quiz).first()
        if attempt:
            f_participation_status[quiz.id] = True
        else:
            f_participation_status[quiz.id] = False

    return render(request, 'user/home.html', {
        'f_quizzes': f_quizzes, 'f_participation_status': f_participation_status
        }
    )

@login_required
def quizes(request):
    user = request.user
    user_course = request.user.course
    quizzes = QuestionPattern.objects.filter(subject__course=user_course).select_related('subject__course').all()
    participation_status = {}

    for quiz in quizzes:
        attempt = UserAttempt.objects.filter(user=user, question__pattern=quiz).first()
        if attempt:
            participation_status[quiz.id] = True
        else:
            participation_status[quiz.id] = False


    return render(request, 'user/quizes.html', {
        'quizzes': quizzes, 'participation_status': participation_status
        }
    )
