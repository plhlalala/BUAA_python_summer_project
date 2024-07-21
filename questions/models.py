from django.db import models
from django.conf import settings


class Chapter(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    FORMAT_CHOICES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image')
    ]

    MULTIPLE_CHOICE = 'mcq'
    OPEN_ENDED = 'open'
    QUESTION_TYPE_CHOICES = [
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (OPEN_ENDED, 'Open Ended')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    format = models.CharField(max_length=5, choices=FORMAT_CHOICES)
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPE_CHOICES)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    correct_answer = models.TextField(blank=True)
    chapters = models.ManyToManyField(Chapter)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_questions', blank=True)

    def __str__(self):
        return self.title


class MultipleChoiceOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class QuestionSet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(Question, related_name='question_sets')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_question_sets', blank=True)

    def __str__(self):
        return self.name
