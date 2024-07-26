from datetime import timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from questions.models import UserAnswer


@login_required
def home(request):
    user = request.user

    # 获取用户完成的题目数量
    completed_questions = UserAnswer.objects.filter(user=user).count()

    # 假设每道题平均花费5分钟计算学习时长
    average_time_per_question = 5  # 分钟
    study_duration_minutes = completed_questions * average_time_per_question
    study_duration = str(timedelta(minutes=study_duration_minutes))

    # 计算技能提升百分比
    total_questions = UserAnswer.objects.filter(user=user).count()
    correct_answers = UserAnswer.objects.filter(user=user, is_correct=True).count()
    skill_improvement = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    skill_improvement = round(skill_improvement, 2)
    context = {
        'completed_questions': completed_questions,
        'study_duration': study_duration,
        'skill_improvement': skill_improvement,
    }
    return render(request, 'home.html', context)
