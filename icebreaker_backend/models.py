from django.db import models


class Picture(models.Model):
    picture = models.ImageField(upload_to='images/uploads', default='images/default/no-img.jpg')


class Blocked(models.Model):
    enroll = models.CharField(max_length=12)


class Contacts(models.Model):
    enroll = models.CharField(max_length=12)


class User(models.Model):
    enroll = models.CharField(max_length=12)
    gender = models.CharField(max_length=6)
    branch = models.CharField(max_length=20)
    college = models.CharField(max_length=20)
    batch = models.CharField(max_length=4, default="B7")
    picture = models.ForeignKey(Picture, null=True)
    blocked = models.ManyToManyField(Blocked, blank=True)
    contacts = models.ManyToManyField(Contacts)
    pic_url = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=200,null=True, default="Hey there! I am using icebreaker.")


class Random(models.Model):
    enroll = models.CharField(max_length=12)
    gender = models.CharField(max_length=6)
    time = models.BigIntegerField(default=123456789)
