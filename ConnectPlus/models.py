from django.db import models

# Create your models here.
class Userinfo(models.Model):
	login_method = models.CharField(max_length = 255, blank = True, null = True)
	email = models.CharField(max_length = 255, blank = True, null = True)
	role = models.CharField(max_length = 255, blank = True, null = True)
	pair = models.ForeignKey('self', blank = True, null = True)
	start_date = models.DateField(blank = True, null = True)
	username = models.CharField(max_length = 255, blank = True, null = True)


class Task(models.Model):
	title = models.CharField(max_length = 255, blank = True, null = True)
	detail = models.CharField(max_length = 1000, blank = True, null = True)
	created_at = models.DateField(blank = True, null = True)
	deadline = models.DateField(blank = True, null = True)
	finished_at = models.DateTimeField(blank = True, null = True)
	status = models.CharField(max_length = 20, blank = True, null = True)
	created_by = models.ForeignKey(User, blank = True, null = True, related_name = 'user_create')
	shared_with = models.ForeignKey(User, blank = True, null = True, related_name = 'user_share')

class Healthlog(models.Model):
	title = models.CharField(max_length = 255, blank = True, null = True)
	detail = models.CharField(max_length = 255, blank = True, null = True)
	created_at = models.DateTimeField(blank = True, null = True)
	created_by = models.ForeignKey(User, blank = True, null = True, related_name = 'user_create')
	shared_with = models.ForeignKey(User, blank = True, null = True, related_name = 'user_share')