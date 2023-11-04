from django.db import models

class Ombor(models.Model):
    nom = models.CharField(max_length=150)
    tel = models.CharField(max_length=13, null=True, blank=True)
    manzil = models.CharField(max_length=255)
    rasm = models.ImageField(upload_to='filial', blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Mahsulot(models.Model):
    nom = models.CharField(max_length=150)
    brand = models.CharField(max_length=150, null=True, blank=True)
    rasm = models.ImageField(upload_to='mahsulot', blank=True, null=True)
    batafsil = models.TextField(null=True, blank=True)
    narx1 = models.FloatField()
    narx2 = models.FloatField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} | {self.brand}"


class Mahsulot_tarqatish(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE, related_name='tarqatmalar')
    ombor = models.ForeignKey(Ombor, on_delete=models.CASCADE, related_name='mahsulot_tarqatmalar')
    miqdor = models.PositiveIntegerField()
    sana = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.mahsulot.__str__()} - {self.ombor.__str__()}"





