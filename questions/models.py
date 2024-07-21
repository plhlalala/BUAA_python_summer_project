# from django.db import models
# from django.contrib.auth.models import User
#
#
# class QuestionGroup(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_public = models.BooleanField(default=False)
#     shared_with = models.ManyToManyField(User, related_name='shared_question_groups')
#
#
# class Question(models.Model):
#     MULTIPLE_CHOICE = 'MC'
#     FILL_IN_THE_BLANK = 'FB'
#     SHORT_ANSWER = 'SA'
#     PROOF = 'PR'
#     QUESTION_TYPES = [
#         (MULTIPLE_CHOICE, '选择题'),
#         (FILL_IN_THE_BLANK, '填空题'),
#         (SHORT_ANSWER, '简答题'),
#         (PROOF, '证明题'),
#     ]
#     group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
#     text = models.TextField()
#     markdown_text = models.TextField(blank=True)
#     image = models.ImageField(upload_to='questions/images/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     text = models.CharField(max_length=255)
#     is_correct = models.BooleanField(default=False)
#
#
# class AnswerLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     is_correct = models.BooleanField()
#     answered_at = models.DateTimeField(auto_now_add=True)
