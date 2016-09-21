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


class Random():
    male = []
    female = []

    def __init__(self):
        pass

    def insert_male(self, enroll):
        if enroll in self.male:
            print enroll
        else:
            self.male.append(enroll)
            print self.male

    def insert_female(self, enroll):
        if enroll in self.female:
            print enroll
        else:
            self.female.append(enroll)
        print self.female

    def get_male(self):

        if len(self.male) == 0:
            data = 'wait'
        else:
            self.male.reverse()
            data = self.male.pop()
            self.male.reverse()
        return data

    def get_female(self):

        if len(self.female) == 0:
            data = 'wait'
        else:
            self.female.reverse()
            data = self.female.pop()
            self.female.reverse()
        return data

    def slice_male(self, enroll):
        if enroll in self.male:
            self.male.remove(enroll)

    def slice_female(self, enroll):
        if enroll in self.female:
            self.female.remove(enroll)
