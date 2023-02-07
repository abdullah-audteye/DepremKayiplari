from django.db import models


class TagArabic(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class IhbarUser(models.Model):
    ihbar_first_name = models.CharField(max_length=100)
    ihbar_last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    eposta = models.EmailField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.ihbar_first_name + " - "+self.ihbar_last_name

class KayipUser(models.Model):
    kayip_first_name = models.CharField(max_length=100)
    kayip_last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    cordinate_x = models.FloatField(max_length=10,blank=True,null=True)
    cordinate_y = models.FloatField(max_length=10,blank=True,null=True)
    address = models.TextField()
    tags = models.ManyToManyField(Tag,blank=True)
    detail = models.TextField(null=True,blank=True)
    status = models.CharField(blank=True,null=True,max_length=255)

    def __str__(self):
        return self.kayip_first_name + " - "+self.kayip_last_name


class Ihbar(models.Model):
    ihbar_user = models.ForeignKey(IhbarUser, on_delete=models.CASCADE,null=True,blank=True)
    kayip_user = models.ManyToManyField(KayipUser)







