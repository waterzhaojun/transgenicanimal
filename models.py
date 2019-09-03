# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from . import utils

from datetime import datetime
import math
import django.urls as urls

# import sys
# sys.path.append('..\\astrotate')
from astrotate.transgenic import transgenic_offspring_name_style as name_style

class TransgenicAnimalLog(models.Model):
    animalid = models.CharField(primary_key=True, max_length=50)
    cageid = models.CharField(max_length=20)
    dob = models.DateField(blank=True, null=True)
    ear_punch = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    birth_mate = models.ForeignKey('TransgenicMouseBreeding', models.DO_NOTHING, blank=True, null=True)
    genotype = models.TextField(blank=True, null=True)
    test_company = models.CharField(max_length=20, blank=True, null=True)
    plate_num = models.CharField(max_length=20, blank=True, null=True)
    #full_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'transgenic_animal_log'

    @property
    def strain(self):
        return(name_style.name_title(self.animalid))

    @property
    def age(self):
        today = datetime.now().date()
        value = math.floor(((today - self.dob).days)/7)
        return(str(value)+ ' weeks')

    # def get_absolute_url(self):
    #     return urls.reverse('index')
    

class TransgenicMouseBreeding(models.Model):
    mateid = models.CharField(primary_key=True, max_length=50)
    cageid = models.CharField(max_length=20)
    father = models.ForeignKey(TransgenicAnimalLog, models.DO_NOTHING, blank=True, null=True, related_name = 'father')
    mother = models.ForeignKey(TransgenicAnimalLog, models.DO_NOTHING, blank=True, null=True, related_name = 'mother')
    pair_date = models.DateField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    weaning_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    inprocess = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transgenic_mouse_breeding'

    def get_absolute_url(self):
        return urls.reverse('index')#, kwargs={'pk': self.pk}) # when update or create finished , where to go. 'index' means go to transgenicanimal index.
        # you can also use a success_url in views. But I think an extra page is useless.

    
class TransgenicAnimalPurchaseinfo(models.Model):
    animalid = models.ForeignKey(TransgenicAnimalLog, models.DO_NOTHING, db_column='animalid', blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    stock_number = models.CharField(max_length=20, blank=True, null=True)
    deliever_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transgenic_animal_purchaseinfo'