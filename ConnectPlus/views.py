from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response

from ConnectPlus.models import *
from ConnectPlus.serializers import *
from django.db.models import Q
# Create your views here.


class TaskView(views.APIView):
    
    def post(self,request,format=None):


    def get(self,request,format=None):
        all_tasks = Task.objects.filter(Q(created_by=request.user)|Q(shared_with=request.user)).ordered_by('-deadline')
        serializer = self.TaskSerializer(all_tasks, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
