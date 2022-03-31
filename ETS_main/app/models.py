from operator import mod
from django.db import models


# Create your models here.
class user(models.Model):
    fullname=models.CharField(max_length=150, null=True, blank=False)
    username=models.CharField(max_length=30, null=False, blank=False, unique=True)
    email=models.CharField(max_length=60, null=False, blank=False)
    password=models.CharField(max_length=55, null=False, blank=False)

class liked_songs(models.Model):
    username=models.ForeignKey(user, to_field='username',on_delete=models.PROTECT, db_column='username')
    track_id=models.CharField(max_length=250, null=False, blank=False, unique=True)
    album_id=models.CharField(max_length=250,null=False, blank=False)

class search_history(models.Model):
    username=models.ForeignKey(user, to_field='username',on_delete=models.PROTECT, db_column='username')
    search_query=models.CharField(max_length=250, null=False, blank=False)
    

class videos_watched(models.Model):
    video_id=models.CharField(max_length=250, null=False, blank=False)
    username=models.ForeignKey(user, to_field='username',on_delete=models.PROTECT, db_column='username')
    