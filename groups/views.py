from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from questions.models import QuestionSet
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
    group = get_object_or_404(Group, id=group_id)
    all_question_sets = QuestionSet.objects.filter(creator=request.user)
    return render(request, 'groups/detail_group.html', {
        'group': group,
        'all_question_sets': all_question_sets,
        'shared_question_sets': group.shared_question_sets.all(),
    })


@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user == group.creator:
        # 删除该组及其所有成员关系
        group.delete()
        return JsonResponse({'success': True, 'message': '小组已删除', 'redirect_url': '/groups/management/'})
    else:
        # 如果用户不是创建者，则删除用户与该组的关系
        group.members.remove(request.user)
        return JsonResponse({'success': True, 'message': '已退出小组', 'redirect_url': '/groups/management/'})


@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)
    return JsonResponse({'success': True, 'message': '已加入小组'})


@login_required
def share_question_set(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        question_set_ids = request.POST.getlist('question_set_ids')
        for qs_id in question_set_ids:
            question_set = get_object_or_404(QuestionSet, id=qs_id)
            question_set.shared_with_groups.add(group)
        return JsonResponse({'success': True, 'message': '题单已共享'})
    return JsonResponse({'success': False, 'message': '请求无效'})
