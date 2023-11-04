from django.db import models
from mainApp.models import Mahsulot, Ombor
from userApp.models import Xodim


class Sotuv(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE, related_name='sotuvlar')
    ombor = models.ForeignKey(Ombor, on_delete=models.CASCADE, related_name='sotuvlar')
    xodim = models.ForeignKey(Xodim, on_delete=models.CASCADE, related_name='sotuvlar')
    miqdor = models.PositiveIntegerField()
    sana = models.DateField()

    def __str__(self):
        return f"{self.mahsulot.__str__()} - {self.ombor.__str__()}"


class Maosh(models.Model):
    xodim = models.ForeignKey(Xodim, on_delete=models.CASCADE, related_name="maoshlar")
    miqdor = models.PositiveIntegerField()
    izoh = models.TextField(blank=True, null=True)
    sana = models.DateField()

    def __str__(self):
        return f"{self.miqdor} | {self.xodim.__str__()}"


class Chiqim(models.Model):
    izoh = models.TextField()
    miqdor = models.PositiveIntegerField()
    ombor = models.ForeignKey(Ombor, on_delete=models.CASCADE, related_name='chiqimlar')
    sana = models.DateField()

    def __str__(self):
        return f"{self.miqdor} | {self.izoh[:50]}"
