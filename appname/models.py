from django.db import models
from datetime import datetime
from django.utils import timezone


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Tagler'
        verbose_name_plural = 'Tagler'




class KayipStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kayıp Durumları'
        verbose_name_plural = 'Kayıp Durumları'


class Countries(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ülkeler'
        verbose_name_plural = 'Ülkeler'


class IhbarUser(models.Model):
    ihbar_first_name = models.CharField(max_length=100)
    ihbar_last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    eposta = models.EmailField(max_length=100,null=True,blank=True)
    country = models.ForeignKey(Countries,null=True,blank=True,on_delete=models.CASCADE)


    def __str__(self):
        return self.ihbar_first_name + " - "+self.ihbar_last_name

    class Meta:
        verbose_name = 'Ihbar Eden Kişiler'
        verbose_name_plural = 'Ihbar Eden Kişiler'


class KayipUser(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    kayip_first_name = models.CharField(max_length=100,db_index=True)
    kayip_last_name = models.CharField(max_length=100)
    cordinate_x = models.FloatField(max_length=10,blank=True,null=True)
    cordinate_y = models.FloatField(max_length=10,blank=True,null=True)
    address = models.TextField(null=True,blank=True)
    tags = models.ManyToManyField(Tag,blank=True)
    detail = models.TextField(null=True,blank=True)
    status = models.CharField(blank=True,null=True,max_length=255)
    kayip_status = models.ForeignKey(KayipStatus,on_delete=models.CASCADE,null=True,blank=True,related_name="kayiplar")
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True,blank=True)
    age = models.IntegerField(null=True,blank=True,default=0)
    created_at = models.DateTimeField(blank=True,null=True,default=timezone.now)


    def __str__(self):
        return self.kayip_first_name + " - "+self.kayip_last_name

    class Meta:
        verbose_name = 'Kaybolan Kişiler'
        verbose_name_plural = 'Kaybolan Kişiler'


class Ihbar(models.Model):
    ihbar_user = models.ForeignKey(IhbarUser, on_delete=models.CASCADE,null=True,blank=True)
    kayip_user = models.ManyToManyField(KayipUser)
    access_code = models.IntegerField(null=True,blank=True,db_index=True)
    created_time = models.DateTimeField(auto_created=True,blank=True,null=True)


    class Meta:
        verbose_name = 'Ihbar'
        verbose_name_plural = 'Ihbarlar'







