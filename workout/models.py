from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Exercise_add(models.Model):
    Exercise = models.CharField(max_length=500)
    Reps = models.IntegerField()
    Sets = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    Description = models.CharField(max_length=100)


class Exercise_list(models.Model):
    sl_no = models.IntegerField(unique=True)
    Exercise = models.CharField(max_length=500)

    def __str__(self):
        return self.Exercise

