from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question, QuestionSet
from .forms import QuestionForm, QuestionSetForm, QuestionSearchForm


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
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.creator = request.user
            question.save()
            form.save_m2m()
            return JsonResponse({'success': True, 'message': '问题已创建', 'question_id': question.id})
        return JsonResponse({'success': False, 'message': '创建问题失败'})
    else:
        form = QuestionForm()
    return render(request, 'questions/create_question.html', {'form': form})


@login_required
def add_option(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        option_text = request.POST.get('option_text')
        is_correct = request.POST.get('is_correct') == 'on'

        option = MultipleChoiceOption.objects.create(
            question=question,
            option_text=option_text,
            is_correct=is_correct
        )
        return JsonResponse(
            {'success': True, 'message': '选项已添加', 'option_text': option.option_text, 'is_correct': is_correct})
    return JsonResponse({'success': False, 'message': '添加选项失败'})


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
    return render(request, 'questions/detail_question.html', {'question': question})


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


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question, QuestionSet
from .forms import QuestionForm, QuestionSetForm, QuestionSearchForm


@login_required
def question_set_detail(request, question_set_id):
    question_set = get_object_or_404(QuestionSet, id=question_set_id)

    if request.method == 'GET':
        search_form = QuestionSearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            search_results = Question.objects.filter(title__icontains=query)
        else:
            search_results = Question.objects.none()
    else:
        search_results = Question.objects.none()
        search_form = QuestionSearchForm()

    return render(request, 'questions/detail_question_set.html', {
        'question_set': question_set,
        'search_form': search_form,
        'search_results': search_results,
        'available_questions': Question.objects.filter(creator=request.user).exclude(question_sets=question_set)
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
