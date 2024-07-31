import json
import os

from django.core.paginator import Paginator
from django.db.models.functions import TruncDate
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden

from groups.models import Group
from . import models
from .models import Question, QuestionSet, UserAnswer
from .forms import QuestionForm, QuestionSetForm, QuestionSearchForm, QuestionPictureForm, CommentForm
import pytesseract
from PIL import Image, ImageEnhance
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserAnswer, Question
from django.db.models import Count, Avg, Q
from django.utils import timezone
import datetime
from .models import SUBJECT_CHOICES
from sensitive_word_filter import DFAFilter


@login_required
def question_management(request):
    search_query = request.GET.get('search', '')
    if search_query:
        search_results = Question.objects.filter(title__icontains=search_query)
        search_performed = True
    else:
        search_results = []
        search_performed = False

    user_questions = Question.objects.filter(creator=request.user)
    user_question_sets = QuestionSet.objects.filter(creator=request.user)

    return render(request, 'questions/management_question.html', {
        'user_questions': user_questions,
        'user_question_sets': user_question_sets,
        'search_results': search_results,
        'search_performed': search_performed
    })


@login_required
def create_question(request):
    if request.method == 'POST':
        if 'format' in request.POST and request.POST['format'] == 'image':
            form = QuestionPictureForm(request.POST, request.FILES)
        else:
            form = QuestionForm(request.POST, request.FILES)

        if form.is_valid():
            question = form.save(commit=False)
            question.creator = request.user
            # 使用 DFAFilter 过滤问题描述和正确答案
            dfa_filter = DFAFilter()
            filtered_description, has_sensitive_word_desc = dfa_filter.filter(question.description)
            filtered_correct_answer, has_sensitive_word_ans = dfa_filter.filter(question.correct_answer)

            if has_sensitive_word_desc or has_sensitive_word_ans:
                return render(request, 'questions/create_question.html', {
                    'form': form,
                    'SUBJECT_CHOICES': models.SUBJECT_CHOICES,
                    'error_message': '问题描述或答案中包含敏感词，请修改后再提交。'
                })

            question.description = filtered_description
            question.correct_answer = filtered_correct_answer
            question.save()
            form.save_m2m()
            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm()

    return render(request, 'questions/create_question.html', {
        'form': form,
        'SUBJECT_CHOICES': models.SUBJECT_CHOICES
    })


@login_required
def ocr_image(request):
    if request.method == 'POST' and request.FILES.get('ocr_image'):
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        image = request.FILES['ocr_image']
        img = Image.open(image)
        img = img.convert('L')  # 转换为灰度图
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)  # 提高对比度
        img = img.point(lambda x: 0 if x < 140 else 255)  # 二值化
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, lang='chi_sim', config=custom_config)
        return JsonResponse({'success': True, 'text': text})
    return JsonResponse({'success': False, 'message': 'OCR识别失败'})


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        if question.creator == request.user:
            question.delete()
            return JsonResponse({'success': True, 'message': '问题已删除'})
        else:
            return JsonResponse({'success': False, 'message': '你没有权限删除此问题'})
    return JsonResponse({'success': False, 'message': '请求无效'})


@login_required
def share_question_set(request, question_set_id):
    question_set = get_object_or_404(QuestionSet, id=question_set_id)
    if request.method == 'POST':
        group_ids = request.POST.getlist('group_ids')
        groups = Group.objects.filter(id__in=group_ids)
        question_set.shared_with_groups.set(groups)
        # 处理复选框的值
        is_public = request.POST.get('is_public') == 'on'
        question_set.is_public = is_public
        question_set.save()
        return JsonResponse({'success': True, 'message': '题组已共享'})
    return JsonResponse({'success': False, 'message': '请求无效'})


@login_required
def delete_question_set(request, question_set_id):
    question_set = get_object_or_404(QuestionSet, id=question_set_id, creator=request.user)
    if request.method == 'POST':
        question_set.delete()
        return JsonResponse({'success': True, 'message': '题单已删除'})
    return JsonResponse({'success': False, 'message': '请求无效'})


@login_required
def share_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.shared_with.add(request.user)
        return JsonResponse({'success': True, 'message': '问题已成功分享'})
    return JsonResponse({'success': False, 'message': '分享失败'})


@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    user = request.user

    # 获取用户所在的组的 ID 列表
    user_group_ids = list(user.joined_groups.values_list('id', flat=True))

    # 检查用户是否有权限访问
    has_access = (
            question.creator == user or
            QuestionSet.objects.filter(questions=question, is_public=True).exists() or
            QuestionSet.objects.filter(questions=question, shared_with_groups__id__in=user_group_ids).exists()
    )
    if not has_access:
        return HttpResponseForbidden("You do not have permission to view this question.")

    comments = question.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.question = question
            comment.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = CommentForm()

    return render(request, 'questions/detail_question.html', {
        'question': question,
        'comments': comments,
        'comment_form': form,
    })


@login_required
def create_question_set(request):
    if request.method == 'POST':
        form = QuestionSetForm(request.POST)
        if form.is_valid():
            question_set = form.save(commit=False)
            question_set.creator = request.user
            question_set.save()
            return JsonResponse({'success': True, 'message': '题单已创建', 'question_set_id': question_set.id})
        return JsonResponse({'success': False, 'message': '创建题单失败'})
    else:
        form = QuestionSetForm()
    return render(request, 'questions/create_question_set.html', {'form': form})


@login_required
def question_set_detail(request, question_set_id):
    question_set = get_object_or_404(QuestionSet, id=question_set_id)
    user = request.user
    # 检查用户是否有权限访问
    user_groups = user.joined_groups.all()
    has_access = (
            question_set.creator == user or
            question_set.is_public or
            question_set.shared_with_groups.filter(id__in=user_groups).exists()
    )
    if not has_access:
        return HttpResponseForbidden("You do not have permission to view this question set.")

    search_results = []
    search_form = QuestionSearchForm(request.GET or None)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        search_results = Question.objects.filter(title__icontains=query).exclude(question_sets=question_set)

    available_questions = Question.objects.filter(creator=request.user).exclude(question_sets=question_set)

    return render(request, 'questions/detail_question_set.html', {
        'question_set': question_set,
        'search_form': search_form,
        'search_results': search_results,
        'available_questions': available_questions,
        'all_groups': Group.objects.all(),
    })


@login_required
def add_question_to_set(request, question_set_id):
    if request.method == 'POST':
        question_set = get_object_or_404(QuestionSet, id=question_set_id)
        question_ids = request.POST.getlist('question_ids')
        questions = Question.objects.filter(id__in=question_ids)
        for question in questions:
            question_set.questions.add(question)
        return JsonResponse({'success': True, 'message': '问题已添加到题单'})
    return JsonResponse({'success': False, 'message': '请求无效'})


@login_required
def remove_question_from_set(request, question_set_id, question_id):
    if request.method == 'POST':
        question_set = get_object_or_404(QuestionSet, id=question_set_id)
        question = get_object_or_404(Question, id=question_id)
        question_set.questions.remove(question)
        return JsonResponse({'success': True, 'message': '问题已从题单中删除'})
    return JsonResponse({'success': False, 'message': '请求无效'})


@login_required
def practice_question_set(request, question_set_id):
    question_set = get_object_or_404(QuestionSet, id=question_set_id)
    user = request.user
    # 检查用户是否有权限访问
    user_groups = user.joined_groups.all()
    has_access = (
            question_set.creator == user or
            question_set.is_public or
            question_set.shared_with_groups.filter(id__in=user_groups).exists()
    )
    if not has_access:
        return HttpResponseForbidden("You do not have permission to view this question set.")
    questions = question_set.questions.all()
    questions_data = [
        {
            'id': question.id,
            'title': question.title,
            'description': question.description,
            'description_image': question.description_image.url if question.description_image else None,
            'image': question.image.url if question.image else None,
            'correct_answer': question.correct_answer,
            'correct_answer_image': question.correct_answer_image.url if question.correct_answer_image else None,
        }
        for question in questions
    ]
    return render(request, 'questions/practice_question_set.html', {
        'question_set': question_set,
        'questions': questions_data,
    })


@login_required
def check_answer(request, question_id):
    if request.method == 'POST':
        user = request.user
        question = get_object_or_404(Question, id=question_id)
        data = json.loads(request.body)
        is_correct = data.get('is_correct')
        wrong_answer_reason = data.get('wrong_answer_reason', '')

        UserAnswer.objects.create(
            user=user,
            question=question,
            is_correct=is_correct,
            wrong_answer_reason=wrong_answer_reason
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


from django.core.paginator import Paginator


@login_required
def question_set_list(request):
    user = request.user
    search_query = request.GET.get('search', '')
    set_search_query = request.GET.get('set_search', '')

    # 获取用户所在的小组的 ID 列表
    group_ids = list(user.joined_groups.values_list('id', flat=True))

    # 获取用户可访问的题单
    accessible_question_sets = QuestionSet.objects.filter(
        Q(creator=user) |
        Q(shared_with_groups__in=group_ids) |
        Q(is_public=True)
    ).distinct()

    # 获取用户可访问的题目
    accessible_questions = Question.objects.filter(
        Q(creator=user) |
        Q(question_sets__in=accessible_question_sets)
    ).distinct()

    if search_query:
        questions = accessible_questions.filter(title__icontains=search_query).distinct()
        search_performed = True
    else:
        questions = []
        search_performed = False

    if set_search_query:
        filtered_question_sets = accessible_question_sets.filter(name__icontains=set_search_query).distinct()
        set_search_performed = True
    else:
        filtered_question_sets = accessible_question_sets
        set_search_performed = False

    # 分页处理
    paginator = Paginator(questions, 5)  # 每页显示5个题目
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'questions/question_set_list.html', {
        'question_sets': accessible_question_sets,
        'filtered_question_sets': filtered_question_sets,
        'questions': page_obj,  # 传递分页对象到模板
        'search_performed': search_performed,
        'set_search_performed': set_search_performed,
        'search_query': search_query,
        'set_search_query': set_search_query
    })


@login_required
def review_mistakes(request):
    user = request.user
    selected_subject = request.GET.get('subject')
    num_questions = int(request.GET.get('num_questions', 5))
    wrong_answers = UserAnswer.objects.filter(user=user, is_correct=False).order_by('-timestamp')
    paginator = Paginator(wrong_answers, 5)  # 每页显示5个错题
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    mistakes = wrong_answers.filter(question__subject=selected_subject)
    mistakes_count = mistakes.values('question').annotate(total=Count('id')).filter(total__gte=2)
    high_mistake_questions = Question.objects.filter(id__in=[item['question'] for item in mistakes_count])
    if high_mistake_questions.count() < num_questions:
        recent_mistakes = mistakes.order_by('-timestamp')[:num_questions]
        recent_mistake_question_ids = [mistake.question_id for mistake in recent_mistakes]
        question_sets = QuestionSet.objects.filter(questions__in=recent_mistake_question_ids).distinct()
        additional_questions = Question.objects.filter(question_sets__in=question_sets,
                                                       subject=selected_subject).exclude(
            id__in=high_mistake_questions).distinct()
        recommended_questions = list(high_mistake_questions) + list(additional_questions)[
                                                               :num_questions - high_mistake_questions.count()]
    else:
        recommended_questions = high_mistake_questions[:num_questions]

    return render(request, 'questions/review_mistakes.html', {
        'page_obj': page_obj,
        'recommended_questions': recommended_questions,
        'subject_choices': SUBJECT_CHOICES,
        'selected_subject': selected_subject,
        'num_questions': num_questions
    })


@login_required
def user_statistics(request):
    user = request.user

    # 获取用户最近30天的答题数据
    today = timezone.now().date()
    last_30_days = today - datetime.timedelta(days=30)
    answers = UserAnswer.objects.filter(user=user, timestamp__date__gte=last_30_days)

    # 每日做题数目
    daily_answers = answers.annotate(date=TruncDate('timestamp')).values('date').annotate(count=Count('id')).order_by(
        'date')

    # 每日做题正确率
    daily_correct_rate = answers.annotate(date=TruncDate('timestamp')).values('date').annotate(
        correct_rate=Avg('is_correct')).order_by('date')
    daily_correct_rate = [{'date': item['date'], 'correct_rate': item['correct_rate'] * 100} for item in
                          daily_correct_rate]

    # 最近7天的正确率
    last_7_days = today - datetime.timedelta(days=7)
    recent_answers = answers.filter(timestamp__date__gte=last_7_days)
    recent_correct_rate = recent_answers.aggregate(average_correct_rate=Avg('is_correct'))[
                              'average_correct_rate'] * 100 if recent_answers.exists() else 0

    # 鼓励语
    if recent_correct_rate >= 90:
        encouragement = "你的表现非常出色，继续保持！"
    elif recent_correct_rate >= 70:
        encouragement = "你的进步很大，继续努力！"
    elif recent_correct_rate >= 50:
        encouragement = "你在逐渐进步，加油！"
    else:
        encouragement = "不要灰心，继续努力，你会看到进步的！"

    # 用户最喜欢做什么题的饼形图数据
    subject_answers = answers.values('question__subject').annotate(count=Count('id')).order_by('-count')

    # 错题科目分布图
    subject_mistakes = answers.filter(is_correct=False).values('question__subject').annotate(
        count=Count('id')).order_by('-count')

    # 将科目翻译为中文
    subject_translation = dict(SUBJECT_CHOICES)
    subject_answers = [{'subject': subject_translation[item['question__subject']], 'count': item['count']} for item in
                       subject_answers]
    subject_mistakes = [{'subject': subject_translation[item['question__subject']], 'count': item['count']} for item in
                        subject_mistakes]

    return render(request, 'questions/user_statistics.html', {
        'daily_answers': daily_answers,
        'daily_correct_rate': daily_correct_rate,
        'subject_answers': subject_answers,
        'subject_mistakes': subject_mistakes,
        'subject_choices': SUBJECT_CHOICES,
        'encouragement': encouragement
    })
