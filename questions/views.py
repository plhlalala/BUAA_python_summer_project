# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import QuestionGroup, Question, Choice, UserAnswer
# from .forms import QuestionGroupForm, QuestionForm, ChoiceFormSet, UploadFileForm
# from django.contrib import messages
# import pytesseract
# from PIL import Image
# import io
#
#
# @login_required
# def create_question(request, group_pk):
#     question_group = get_object_or_404(QuestionGroup, pk=group_pk)
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         formset = ChoiceFormSet(request.POST)
#         if form.is_valid() and formset.is_valid():
#             question = form.save(commit=False)
#             question.group = question_group
#             question.created_by = request.user
#             question.save()
#             formset.instance = question
#             formset.save()
#             return redirect('question_group_detail', pk=group_pk)
#     else:
#         form = QuestionForm()
#         formset = ChoiceFormSet()
#     return render(request, 'questions/create_question.html', {
#         'form': form,
#         'formset': formset,
#         'question_group': question_group
#     })
#
#
# @login_required
# def create_question_group(request):
#     if request.method == 'POST':
#         form = QuestionGroupForm(request.POST)
#         if form.is_valid():
#             question_group = form.save(commit=False)
#             question_group.creator = request.user
#             question_group.save()
#             return redirect('question_group_detail', pk=question_group.pk)
#     else:
#         form = QuestionGroupForm()
#     return render(request, 'questions/create_question_group.html', {'form': form})
#
#
# @login_required
# def question_group_detail(request, pk):
#     question_group = get_object_or_404(QuestionGroup, pk=pk)
#     questions = question_group.questions.all()
#     return render(request, 'questions/question_group_detail.html', {
#         'question_group': question_group,
#         'questions': questions
#     })
#
#
# @login_required
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             if file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
#                 image = Image.open(io.BytesIO(file.read()))
#                 text = pytesseract.image_to_string(image)
#             elif file.name.lower().endswith('.pdf'):
#                 # 在此添加PDF处理逻辑
#                 text = "PDF处理尚未实现"
#             else:
#                 messages.error(request, "不支持的文件格式")
#                 return redirect('upload_file')
#
#             return render(request, 'questions/edit_extracted_text.html', {'text': text})
#     else:
#         form = UploadFileForm()
#     return render(request, 'questions/upload_file.html', {'form': form})
#
#
# @login_required
# def take_quiz(request, group_pk):
#     question_group = get_object_or_404(QuestionGroup, pk=group_pk)
#     questions = question_group.questions.all()
#
#     if request.method == 'POST':
#         for question in questions:
#             answer = request.POST.get(f'question_{question.id}')
#             is_correct = False
#             if question.type == 'MC':
#                 correct_choice = question.choices.filter(is_correct=True).first()
#                 is_correct = (answer == str(correct_choice.id))
#             elif question.type == 'FIB':
#                 correct_answer = question.choices.filter(is_correct=True).first().content
#                 is_correct = (answer.lower() == correct_answer.lower())
#
#             UserAnswer.objects.create(
#                 user=request.user,
#                 question=question,
#                 answer=answer,
#                 is_correct=is_correct
#             )
#         return redirect('quiz_results', group_pk=group_pk)
#
#     return render(request, 'questions/take_quiz.html', {
#         'question_group': question_group,
#         'questions': questions
#     })
#
#
# @login_required
# def quiz_results(request, group_pk):
#     question_group = get_object_or_404(QuestionGroup, pk=group_pk)
#     user_answers = UserAnswer.objects.filter(
#         user=request.user,
#         question__group=question_group
#     ).order_by('question')
#
#     return render(request, 'questions/quiz_results.html', {
#         'question_group': question_group,
#         'user_answers': user_answers
#     })
