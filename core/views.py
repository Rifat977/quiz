from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from course.models import *
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    user = request.user
    user_course = request.user.course

    f_quizzes = QuestionPattern.objects.filter(subject__course=user_course, is_featured=True).select_related('subject__course').all()
    f_participation_status = {}

    notification = Notification.objects.filter(is_active=True).first()


    for quiz in f_quizzes:
        attempt = UserAttempt.objects.filter(user=user, question=quiz).first()
        if attempt:
            f_participation_status[quiz.id] = True
        else:
            f_participation_status[quiz.id] = False

    return render(request, 'user/home.html', {
        'f_quizzes': f_quizzes, 'f_participation_status': f_participation_status,
        'notification': notification
        }
    )

@login_required
def quizes(request):
    user = request.user
    user_course = request.user.course
    quizzes = QuestionPattern.objects.filter(subject__course=user_course).select_related('subject__course').all()
    participation_status = {}

    for quiz in quizzes:
        attempt = UserAttempt.objects.filter(user=user, question=quiz).first()
        if attempt:
            participation_status[quiz.id] = True
        else:
            participation_status[quiz.id] = False


    return render(request, 'user/quizes.html', {
        'quizzes': quizzes, 'participation_status': participation_status
        }
    )

@login_required
def quiz(request):
    if request.method == 'POST':
        user = request.user
        q_pattern_id = request.POST.get('quiz')
        q_pattern = QuestionPattern.objects.get(pk=q_pattern_id)
        # if UserAttempt.objects.filter(user=user, question=q_pattern).exists():
            # messages.error(request, "You have already attempted this quiz.")
        #     return redirect("core:home")
        # else:
            # UserAttempt.objects.create(user=user, question=q_pattern, attempt_count=1)
        questions = Question.objects.filter(pattern=q_pattern, visit_count=0)
        return render(request, 'user/quiz.html', {'q_pattern': q_pattern, 'questions': questions})
    return redirect("core:home")


@login_required
def submit_answer(request):
    if request.method == 'POST':
        user = request.user
        score = 0
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(value)
                selected_answer = request.POST.get('customRadio_' + str(question_id))

                print(question_id)
                print(selected_answer)

                question = Question.objects.get(pk=question_id)
                
                if selected_answer == question.correct_answer:
                    score += question.pattern.points 

        print(score)
                
    return redirect('core:home')