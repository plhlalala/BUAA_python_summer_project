from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question, MultipleChoiceOption, QuestionSet
from .forms import QuestionForm, MultipleChoiceOptionForm

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
        return JsonResponse({'success': True, 'message': '选项已添加', 'option_text': option.option_text, 'is_correct': is_correct})
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
        name = request.POST.get('name')
        description = request.POST.get('description')
        question_set = QuestionSet.objects.create(
            name=name,
            description=description,
            creator=request.user
        )
        return JsonResponse({'success': True, 'message': '题单已创建', 'question_set_id': question_set.id})
    return render(request, 'questions/create_question_set.html')

@login_required
def question_set_detail(request, question_set_id):
    question_set = get_object_or_404(QuestionSet, id=question_set_id)
    return render(request, 'questions/detail_question_set.html', {'question_set': question_set})
