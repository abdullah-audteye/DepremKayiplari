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
    country_code = models.CharField(null=True,blank=True,max_length=10)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ülkeler'
        verbose_name_plural = 'Ülkeler'


class Cities(models.Model):
    country = models.ForeignKey(Countries,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50)
    coordinate_x = models.FloatField(max_length=10,blank=True,null=True)
    coordinate_y = models.FloatField(max_length=10,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Şehirler'
        verbose_name_plural = 'Şehirler'


class IhbarUser(models.Model):
    ihbar_first_name = models.CharField(max_length=100)
    ihbar_last_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    eposta = models.EmailField(max_length=100,null=True,blank=True)
    # country = models.ForeignKey(Countries,null=True,blank=True,on_delete=models.CASCADE)


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
    status = models.TextField(null=True,blank=True)
    kayip_status = models.ForeignKey(KayipStatus,on_delete=models.CASCADE,null=True,blank=True,related_name="kayiplar")
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True,blank=True)
    age = models.CharField(null=True,blank=True,max_length=5)
    city = models.ForeignKey(Cities,on_delete=models.CASCADE,null=True,blank=True)


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







