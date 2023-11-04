from django.contrib.auth.models import User
from django.db import models
from mainApp.models import Ombor

class Xodim(models.Model):

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    ism = models.CharField(max_length=150)
    fam = models.CharField(max_length=150, blank=True, null=True)
    ombor = models.ForeignKey(Ombor, on_delete=models.CASCADE, related_name='xodimlar')
    tel = models.CharField(max_length=13)
    kpi = models.FloatField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='xodimlar')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.username

