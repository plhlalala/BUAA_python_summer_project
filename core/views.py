from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from questions.models import Question
# from groups.models import Group

@login_required
def home(request):
    return render(request, 'home.html')