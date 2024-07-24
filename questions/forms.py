from django import forms
from .models import Question, QuestionSet


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'format', 'image', 'correct_answer', 'subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False


class QuestionPictureForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description_image', 'format', 'image', 'correct_answer_image', 'subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['description_image'].required = False
        self.fields['correct_answer_image'].required = False


class QuestionSetForm(forms.ModelForm):
    class Meta:
        model = QuestionSet
        fields = ['name', 'description']


class QuestionSearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label='Search Questions')
