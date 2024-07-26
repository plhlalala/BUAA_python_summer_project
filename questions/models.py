from django.db import models
from django.conf import settings

from groups.models import Group

SUBJECT_CHOICES = [
    ('math_analysis_1', '数学分析上'),
    ('math_analysis_2', '数学分析下'),
    ('linear_algebra', '线性代数'),
    ('physics_1', '大学物理上'),
    ('physics_2', '大学物理下'),
    ('discrete_math_1', '离散数学1'),
    ('discrete_math_2', '离散数学2'),
    ('discrete_math_3', '离散数学3'),
    ('probability_theory', '概率论与数理统计'),
    ('computer_organization', '计算机组成'),
    ('data_structure', '数据结构'),
    ('algorithm', '算法设计与分析'),
    ('operating_system', '操作系统'),
    ('database', '数据库系统'),
    ('computer_network', '计算机网络'),
    ('compiler', '编译原理'),
    ('others', '其他')
]


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
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)

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
