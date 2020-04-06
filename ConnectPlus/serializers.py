from rest_framework import serializers
from ConnectPlus.models import *

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = ('title', 'detail', 'deadline', 'finished_at', 'status',)

class HealthlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Healthlog
		fields = ('title', 'detail', 'created_at')
