from django import forms
from .models import Question, QuestionSet


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'format', 'image', 'correct_answer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False


class QuestionSetForm(forms.ModelForm):
    class Meta:
        model = QuestionSet
        fields = ['name', 'description']


class QuestionSearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label='Search Questions')
