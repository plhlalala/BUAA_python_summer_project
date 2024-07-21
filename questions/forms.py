# from django import forms
# from .models import QuestionGroup, Question, Choice
#
#
# class QuestionGroupForm(forms.ModelForm):
#     class Meta:
#         model = QuestionGroup
#         fields = ['name', 'description', 'is_public']
#
#
# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['type', 'content']
#
#
# class ChoiceForm(forms.ModelForm):
#     class Meta:
#         model = Choice
#         fields = ['content', 'is_correct']
#
#
# ChoiceFormSet = forms.inlineformset_factory(
#     Question, Choice, form=ChoiceForm, extra=4, can_delete=True
# )
#
#
# class UploadFileForm(forms.Form):
#     file = forms.FileField()
