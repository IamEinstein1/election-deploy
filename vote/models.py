from django.db import models

# Create your models here.


class SPL(models.Model):
    name = models.CharField(max_length=2048)
    votes = models.IntegerField(default=0, blank=True)
    img_url = models.CharField(max_length=2048, blank=True)

    def __str__(self):
        return self.name


class ASPL(models.Model):
    name = models.CharField(max_length=2048)
    votes = models.IntegerField(default=0, blank=True)
    img_url = models.CharField(max_length=2048, blank=True)

    def __str__(self):
        return self.name


class Animal(models.Model):
    name = models.CharField(max_length=300)
    sound = models.CharField(max_length=2048)

    def __str__(self):
        return self.name

    def speak(self):
        return f"The {self.name} says \"{self.sound}\""


class User(models.Model):
    # id = models.AutoField(primary_key=False)
    email = models.CharField(null=False, max_length=200, default="mail")
    ip = models.CharField(max_length=200, primary_key=True)
    aspl_done = models.BooleanField(default=False)
    spl_done = models.BooleanField(default=False)
    times_visited = models.IntegerField(default=0, null=False)
