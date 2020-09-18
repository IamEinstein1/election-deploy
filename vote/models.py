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
