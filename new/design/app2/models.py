from django.db import models

# Create your models here.

class Place(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField(default="")
    image=models.ImageField(upload_to="place/image",null=True,blank=True)
    def __str__(self):
        return self.name


class Team(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField(default="")
    image=models.ImageField(upload_to="team/image",null=True,blank=True)
    def __str__(self):
        return self.name



