from django.contrib import admin

# Register your models here.
from .models import TransgenicAnimalLog, TransgenicMouseBreeding

admin.site.register(TransgenicAnimalLog)
admin.site.register(TransgenicMouseBreeding)