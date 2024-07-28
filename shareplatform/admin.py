# shareplatform/admin.py

from django.contrib.admin import AdminSite
from django.contrib import admin
from questions.models import Question, QuestionSet, UserAnswer, Comment
from groups.models import Group
from user.models import User


class CustomAdminSite(AdminSite):
    site_header = "共享练习平台管理"
    site_title = "共享练习平台管理门户"
    index_title = "欢迎来到共享练习平台管理门户"


custom_admin_site = CustomAdminSite(name='custom_admin')


@admin.register(Question, site=custom_admin_site)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'format', 'subject', 'creator')
    list_filter = ('format', 'subject', 'creator')
    search_fields = ('title', 'description', 'correct_answer')


@admin.register(QuestionSet, site=custom_admin_site)
class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'is_public')
    list_filter = ('is_public', 'creator')
    search_fields = ('name', 'description')
    filter_horizontal = ('questions', 'shared_with_groups')


@admin.register(UserAnswer, site=custom_admin_site)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_correct', 'timestamp')
    list_filter = ('is_correct', 'timestamp')
    search_fields = ('user__username', 'question__title', 'wrong_answer_reason')


@admin.register(Comment, site=custom_admin_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at')
    search_fields = ('question__title', 'author__username')


@admin.register(Group, site=custom_admin_site)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at')
    search_fields = ('name', 'description')


@admin.register(User, site=custom_admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'location')
    search_fields = ('username', 'email', 'bio')
