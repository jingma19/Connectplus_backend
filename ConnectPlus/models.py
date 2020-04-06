from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import validators
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from rest_framework.authtoken.models import Token


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        ('email address'),
        unique=True,
        error_messages={
            'unique': ("A user with that email already exists."),
        })
    username = models.CharField(
        ('username'),
        max_length=100,
        unique=True,
        help_text=('Required. 30 characters or fewer. Letters, digits and '
                   '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                ('Enter a valid username. '
                 'This value may contain only letters, numbers '
                 'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': ("A user with that username already exists."),
        })
    role = models.CharField(max_length=10, blank=True)
    partner = models.ForeignKey('self', blank = True, null = True, related_name='partner')
    login_method = models.CharField(max_length = 255, blank = True, null = True)
    start_date = models.DateField(blank = True, null = True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    class Meta:
        managed = True
        abstract = False
        db_table = 'auth_user'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    Token.objects.get_or_create(user=instance)

'''
class Userinfo(models.Model):
    login_method = models.CharField(max_length = 255, blank = True, null = True)
    email = models.CharField(max_length = 255, blank = True, null = True)
    role = models.CharField(max_length = 255, blank = True, null = True)
    pair = models.ForeignKey(User, blank = True, null = True)
    start_date = models.DateField(blank = True, null = True)
    username = models.CharField(max_length = 255, blank = True, null = True)
'''

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