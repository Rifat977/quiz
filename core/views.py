from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from course.models import *
from .models import *
from django.contrib import messages

import json, random

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

    attempt_ids = {}

    for quiz in f_quizzes:
        attempt = UserAttempt.objects.filter(user=user, question=quiz).first()
        if attempt:
            f_participation_status[quiz.id] = True
            attempt_ids[quiz.id] = attempt.id
        else:
            f_participation_status[quiz.id] = False

    return render(request, 'user/home.html', {
        'f_quizzes': f_quizzes,
        'f_participation_status': f_participation_status,
        'notification': notification,
        'attempt_ids': attempt_ids,
    })

@login_required
def quizes(request):
    user = request.user
    user_course = request.user.course
    quizzes = QuestionPattern.objects.filter(subject__course=user_course).select_related('subject__course').all()
    participation_status = {}

    attempt_ids = {}

    for quiz in quizzes:
        attempt = UserAttempt.objects.filter(user=user, question=quiz).first()
        if attempt:
            participation_status[quiz.id] = True
            attempt_ids[quiz.id] = attempt.id
        else:
            participation_status[quiz.id] = False


    return render(request, 'user/quizes.html', {
        'quizzes': quizzes, 'participation_status': participation_status, 'attempt_ids': attempt_ids,
        }
    )

@login_required
def quiz(request):
    if request.method == 'POST':
        user = request.user
        q_pattern_id = request.POST.get('quiz')
        q_pattern = QuestionPattern.objects.get(pk=q_pattern_id)
        if UserAttempt.objects.filter(user=user, question=q_pattern).exists():
            messages.error(request, "You have already attempted this quiz.")
            return redirect("core:home")
        else:
             user_attempt = UserAttempt.objects.create(user=user, question=q_pattern, attempt_count=1)
             if q_pattern.random_serve:
                questions = Question.objects.filter(pattern=q_pattern)
                total_questions_served = min(q_pattern.total_questions_served, questions.count())
                questions = random.sample(list(questions), total_questions_served)
             else:
                questions = Question.objects.filter(pattern=q_pattern).order_by('id')[:q_pattern.total_questions_served]
        return render(request, 'user/quiz.html', {'q_pattern': q_pattern, 'questions': questions})
    return redirect("core:home")


@login_required
def submit_answer(request):
    if request.method == 'POST':
        user = request.user
        score = 0
        user_selected_answers = {}
        questions = {} 

        q_pattern_id = request.POST.get('q_pattern')
        q_pattern = QuestionPattern.objects.get(pk=q_pattern_id)
        try:
            user_attempt = UserAttempt.objects.get(user=user, question=q_pattern, attempt_count=1)
        except UserAttempt.DoesNotExist:
                messages.error(request, "Something went wrong!")
                return redirect("core:home")
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(value)
                selected_answer = request.POST.get('customRadio_' + str(question_id))

                user_selected_answers[question_id] = selected_answer 
                question = Question.objects.get(pk=question_id)
                questions[question_id] = question 

                if selected_answer == question.correct_answer:
                    score += question.pattern.points 
                    is_correct = True
                else:
                    is_correct = False

                UserAnswer.objects.create(
                    user_attempt=user_attempt,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=is_correct
                )

        user.point += score
        user.save()

        return redirect('core:attempt_answer', user_attempt_id=user_attempt.id)

        # if user_selected_answers and questions:
        #     correct_answers = {} 
        #     for question_id, selected_answer in user_selected_answers.items():
        #         question = questions.get(question_id)
        #         correct_answers[question_id] = question.correct_answer
        #     return render(request, 'user/quiz_review.html', {'user_selected_answers': user_selected_answers, 'correct_answers': correct_answers, 'questions': questions, 'score':score})
        # else:
        #     return redirect("core:home")
    return redirect("core:home")

@login_required
def show_user_answers(request, user_attempt_id):
    user_attempt = UserAttempt.objects.get(pk=user_attempt_id, user=request.user)
    user_answers = UserAnswer.objects.filter(user_attempt=user_attempt)

    return render(request, 'user/attempt_answer.html', {'user_answers': user_answers})

@login_required
def wallet(request):
    user = request.user
    per_point = PointSetting.objects.first()
    total_amount = per_point.per_point * user.point
    withdrawals = Withdrawal.objects.filter(user=user).order_by('-id')

    context = {
        'per_point': per_point,
        'user': user,
        'total_amount': total_amount,
        'withdrawals': withdrawals
    }
    return render(request, 'user/wallet.html', context)


@login_required
def withdrawal(request):
    if request.method == 'POST':
        user = request.user
        amount = request.POST.get('amount')
        wallet_address = request.POST.get('wallet_address')
        payment_method = request.POST.get('payment_method')

        point_setting = PointSetting.objects.first()
        per_point = point_setting.per_point
        user_balance = per_point * user.point

        print(user_balance)


        if not amount or not wallet_address or not payment_method:
            messages.error(request, "Input fields must be required")
            return redirect('core:wallet')

        if int(amount) > user_balance:
            messages.error(request, "Insuficcent balance.")
            return redirect('core:wallet')
        else:
            withdrawal = Withdrawal(user=user, amount=amount, wallet_address=wallet_address, payment_method=payment_method)
            withdrawal.save()

        return redirect('core:wallet')

