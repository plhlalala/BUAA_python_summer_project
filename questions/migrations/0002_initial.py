# Generated by Django 4.2.14 on 2024-07-21 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='questionset',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questionset',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='question_sets', to='questions.question'),
        ),
        migrations.AddField(
            model_name='questionset',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_question_sets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='multiplechoiceoption',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='questions.question'),
        ),
    ]
