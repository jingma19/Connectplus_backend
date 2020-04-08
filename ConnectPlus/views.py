from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import facebook
from rest_framework.authtoken.models import Token
import json
import datetime

from ConnectPlus.models import *
from ConnectPlus.serializers import *
from django.db.models import Q
# Create your views here.

@csrf_exempt
def login_fb_action(request):
    print("get request from fb login")
    #data = json.loads(request.body.decode('utf-8'))
    access_token = request.GET['accessToken']
    print("accessToken is ")
    print(access_token)
    new_user = 'False'
    try:
        print("first try")
        graph = facebook.GraphAPI(access_token=access_token)
        user_info = graph.get_object(
            id='me',
            fields='email, id'
            )
    except facebook.GraphAPIError:
        print("first except")
        return JsonResponse({'error': 'Invalid data'}, safe=False)

    try:
        print("second try")
        print(user_info.get('id'))
        user = User.objects.get(facebook_id=user_info.get('id'))

    except User.DoesNotExist:
        print("second except")
        password = User.objects.make_random_password()
        user = User(
            email=user_info.get('email')
            or 'None',
            facebook_id=user_info.get('id'),
            username='Facebook_'+user_info.get('id'),
            login_method='Facebook',
            )
        user.set_password(password)
        user.save()
        new_user = 'True'
    token = Token.objects.get(user=user).key

    if token:
        print(new_user)
        un = 'Facebook_'+user_info.get('id')
        return JsonResponse({'answer': new_user, 'username':un},
                            safe=False)
    else:
        return JsonResponse({'error': 'Invalid data'}, safe=False)

@csrf_exempt
@login_required
def task_action(request):
    return




@csrf_exempt
@login_required
def add_task_action(request):
    username = request.POST['username']
    deadline = request.POST['deadline']
    title = request.POST['title']
    detail = request.POST['detail']

    if not username:
        return JsonResponse({'success': 'False', 'message': 'Missing username.'}, safe=False)

    if not deadline:
        return JsonResponse({'success': 'False', 'message': 'Missing deadline.'}, safe=False)
    if not title:
        return JsonResponse({'success': 'False', 'message': 'Missing task title.'}, safe=False)
    if not detail:
        detail = "None"
    elif len(detail) > 1000:
        return JsonResponse({'success': 'False', 'message': 'Maximum characters for detail is 1000.'}, safe=False)

    user = User.objects.get(username=username)
    if not user:
        return JsonResponse({'success': 'False', 'message': 'Invalid username'}, safe=False)

    new_task = Task(title=title,
                    detail=detail,
                    created_at=datetime.date.today,
                    deadline=datetime.datetime.strptime(deadline, "%Y-%m-%d").date(),
                    status='incompleted',
                    created_by=user,
                    shared_with=User.objects.get(username=user.partner_name),
        )
    new_task.save()
    return JsonResponse({'success': 'True', 'message': 'Task saved successfully.'}, safe=False)

@csrf_exempt
@login_required
def complete_task_action(request):
    return

@csrf_exempt
@login_required
def send_appreciation_action(request):
    return

















