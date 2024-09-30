from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.decorators import login_required
from account.models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action

@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')
    paginator = Paginator(actions, 8)
    page = request.GET.get('page')
    actions_only = request.GET.get('actions_only')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        actions = paginator.page(1)
    except EmptyPage:
        if actions_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        actions = paginator.page(paginator.num_pages)
    if actions_only:
        return render(request,
                      'actions/action/detail.xhtml',
                      {'section': 'dashboard',
                       'actions': actions})
    return render(request, 'account/dashboard.xhtml', { 'section': 'dashboard', 'actions': actions})

def register(request):
    if request.method == 'POST':
        form = User_Registration_Form(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.xhtml', {'newuser': new_user })
    else:
        form = User_Registration_Form()    
    return render(request, 'account/register.xhtml', {'form': form })

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/edit.xhtml',
                  {'user_form': user_form,
                   'profile_form': profile_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    paginator = Paginator(users, 4)
    page = request.GET.get('page')
    users_only = request.GET.get('users_only')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        if users_only:
            return HttpResponse('')
        users = paginator.page(paginator.num_pages)
    if users_only:
        return render(request,
                      'account/user/list_user.xhtml',
                      {'section': 'people',
                       'users': users})
    return render(request,
                  'account/user/list.xhtml',
                  {'section': 'people',
                   'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.xhtml',
                  {'section': 'people',
                   'user': user})

@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})