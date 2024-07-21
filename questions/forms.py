from django import forms
from .models import Question, MultipleChoiceOption, Chapter

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'format', 'question_type', 'image', 'correct_answer', 'chapters']

class MultipleChoiceOptionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceOption
        fields = ['option_text', 'is_correct']
