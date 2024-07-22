from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from questions.models import Question
from .models import Group
from .forms import GroupForm

from django.shortcuts import render


@login_required
def group_management(request):
    user_groups = request.user.joined_groups.all()
    search_query = request.GET.get('search', '')
    search_results = []
    search_performed = False

    if search_query:
        search_results = Group.objects.filter(name__icontains=search_query)
        search_performed = True

    context = {
        'user_groups': user_groups,
        'search_results': search_results,
        'search_performed': search_performed,
    }
    return render(request, 'groups/management_group.html', context)


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.members.add(request.user)
            messages.success(request, 'Group created successfully.')
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})


@login_required
def group_list(request):
    user_groups = request.user.joined_groups.all()
    available_groups = Group.objects.exclude(members=request.user)
    return render(request, 'groups/group_list.html', {'user_groups': user_groups, 'available_groups': available_groups})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    # 暂时注释掉 group_questions 查询
    # group_questions = Question.objects.filter(group=group).order_by('-created_at')[:5]

    # 添加一个占位符
    group_questions = []

    context = {
        'group': group,
        'group_questions': group_questions,
    }
    return render(request, 'groups/detail_group.html', context)


@login_required
def join_group(request, group_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group = get_object_or_404(Group, pk=group_id)
        if request.user not in group.members.all():
            group.members.add(request.user)
            return JsonResponse({'success': True, 'message': f'You have joined the group: {group.name}'})
        else:
            return JsonResponse({'success': False, 'message': 'You are already a member of this group.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def leave_group(request, group_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group = get_object_or_404(Group, pk=group_id)
        if request.user in group.members.all():
            group.members.remove(request.user)
            return JsonResponse({'success': True, 'message': f'You have left the group: {group.name}'})
        else:
            return JsonResponse({'success': False, 'message': 'You are not a member of this group.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})
