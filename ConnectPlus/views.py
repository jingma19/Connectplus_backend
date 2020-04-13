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
from django.core import serializers

from ConnectPlus.models import *
#from ConnectPlus.serializers import *
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
def get_username_from_token(request):
    print("getting username")
    access_token = request.GET['accessToken']
    try:
        print("first try")
        graph = facebook.GraphAPI(access_token=access_token)
        user_info = graph.get_object(
            id='me',
            fields='email, id'
            )
    except facebook.GraphAPIError:
        print("first except")
        return JsonResponse({'success': 'False', 'username':''}, safe=False)

    try:
        print("second try")
        print(user_info.get('id'))
        user = User.objects.get(facebook_id=user_info.get('id'))

    except User.DoesNotExist:
        return JsonResponse({'success': 'False', 'username':''}, safe=False)

    return JsonResponse({'success':'True', 'username': user.username}, safe=False)


@csrf_exempt
def task_action(request):
    # order based on -deadline!
    username = request.GET['unique_username']

    user = User.objects.get(username=username)
    if not user:
        return JsonResponse(status=500, data={'error': 'User does not exist'}, safe=False)

    all_tasks = Task.objects.filter(created_by__username__exact=user.username).order_by('-deadline')
    print(len(all_tasks))
    #json_tasks = serializers.serialize('json', all_tasks)
    #print(json_tasks)
    json_tasks = []
    for t in all_tasks:
        json_t = {}
        json_t['title'] = t.title
        json_t['detail'] = t.detail
        json_t['created_at'] = t.created_at.strftime("%Y-%m-%d")
        json_t['deadline'] = t.created_at.strftime("%Y-%m-%d")
        
        if t.finished_at:
            json_t['finished_at'] = t.finished_at.strftime("%Y-%m-%d %H:%M")
        else:
            json_t['finished_at'] = ""
        json_t['status'] = t.status
        json_tasks.append(json_t)
    print(json.dumps(json_tasks))
    print(json_tasks)
    return JsonResponse(json_tasks, safe=False)




@csrf_exempt
def add_task_action(request):
    print("Get a POST request to add task")
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    

    print(body)
    print(body['title'])

    username = body['unique_username']
    deadline = body['deadline']
    title = body['title']
    detail = body['detail']




    print(request.POST)
    print(request.body)

    if not title:
        print('missing title')
        return JsonResponse({'success': 'False', 'message': 'Missing task title.'}, safe=False)
    
    
    if not deadline:
        return JsonResponse({'success': 'False', 'message': 'Missing deadline.'}, safe=False)
    if not username:
        return JsonResponse({'success': 'False', 'message': 'Missing username.'}, safe=False)

    
    if not detail:
        detail = "None"
    elif len(detail) > 1000:
        return JsonResponse({'success': 'False', 'message': 'Maximum characters for detail is 1000.'}, safe=False)

    user = User.objects.get(username=username)
    if not user:
        return JsonResponse({'success': 'False', 'message': 'Invalid username'}, safe=False)


    
    if not user.partner_name:
        print(datetime.date.today)
        print(datetime.datetime.strptime(deadline, "%Y-%m-%d").date())
        new_task = Task(title=title,
                    detail=detail,
                    created_at=datetime.date.today(),
                    deadline=datetime.datetime.strptime(deadline, "%Y-%m-%d").date(),
                    status='incompleted',
                    created_by=user,
        )
        new_task.save()
    else:
        new_task = Task(title=title,
                    detail=detail,
                    created_at=datetime.date.today(),
                    deadline=datetime.datetime.strptime(deadline, "%Y-%m-%d").date(),
                    status='incompleted',
                    created_by=user,
                    shared_with=User.objects.get(username=user.partner_name),
        )
        new_task.save()
    print("task saved!")
    return JsonResponse({'success': 'True', 'message': 'Task saved successfully.'}, safe=False)

@csrf_exempt
def complete_task_action(request):
    return

@csrf_exempt
def send_appreciation_action(request):
    return

















