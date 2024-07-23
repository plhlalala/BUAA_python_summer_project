from django.db import models
from django.conf import settings

from groups.models import Group


class Question(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    FORMAT_CHOICES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    description_image = models.ImageField(upload_to='questions/', blank=True, null=True)
    format = models.CharField(max_length=5, choices=FORMAT_CHOICES)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    correct_answer = models.TextField(blank=True)
    correct_answer_image = models.ImageField(upload_to='questions/', blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_questions', blank=True)

    def __str__(self):
        return self.title


class QuestionSet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(Question, related_name='question_sets', blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_with_groups = models.ManyToManyField(Group, related_name='shared_question_sets', blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    wrong_answer_reason = models.TextField(blank=True)
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
