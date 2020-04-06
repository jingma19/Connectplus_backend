from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import facebook
from rest_framework.authtoken.models import Token
import json

from ConnectPlus.models import *
from ConnectPlus.serializers import *
from django.db.models import Q
# Create your views here.

@csrf_exempt
def login_fb_action(request):
    data = json.loads(request.body.decode('utf-8'))
    access_token = data.get('accessToken')
    new_user = False
    try:
        graph = facebook.GraphAPI(access_token=access_token)
        user_info = graph.get_object(
            id='me',
            fields='email, id'
            )
    except facebook.GraphAPIError:
        return JsonResponse({'error': 'Invalid data'}, safe=False)

    try:
        user = User.objects.get(facebook_id=user_info.get('id'))

    except User.DoesNotExist:
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
        new_user = True
    token = Token.objects.get(user=user).key
    if token:
        return JsonResponse({'new_user': new_user},
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
    return

@csrf_exempt
@login_required
def complete_task_action(request):
    return

@csrf_exempt
@login_required
def send_appreciation_action(request):
    return

















