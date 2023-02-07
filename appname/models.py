from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=100)
class IhbarUser(models.Model):
    ihbar_first_name = models.CharField(max_length=100)
    ihbar_last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    eposta = models.EmailField(max_length=100)

class KayipUser(models.Model):
    kayip_first_name = models.CharField(max_length=100)
    kayip_last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    cordinate_x = models.FloatField(max_length=10)
    cordinate_y = models.FloatField(max_length=10)
    address = models.TextField()
    tags = models.ManyToManyField(Tag,blank=True)
    detail = models.TextField(null=True,blank=True)


class Ihbar(models.Model):
    ihbar_user = models.ForeignKey(IhbarUser, on_delete=models.CASCADE)
    kayip_user = models.ManyToManyField(KayipUser)






