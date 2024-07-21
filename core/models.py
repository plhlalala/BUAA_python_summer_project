from django.db import models
from user.models import User
# Create your models here.
class StudentAbility(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ability_score = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)
