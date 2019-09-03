from django.urls import path
from django.conf.urls import url
from . import views

# app_name = 'transgenicanimal'

urlpatterns = [

    path('', views.index.as_view(), name='index'),
    path('animalinfo/', views.index.as_view()),
    path('index', views.index.as_view()),
    path('animalinfo/<str:pk>', views.AnimalInfo.as_view(), name='animalinfo'),
    path('animalinfo_create/', views.AnimalCreate.as_view(), name='animal_create'),
    path('createmate/', views.MateCreate.as_view(), name='mate_create'),
    path('mateinfo/<str:pk>', views.MateInfo.as_view(), name='mateinfo'),
    # path('animalinfo/<str:pk>', views.animalinfo(), name = 'animalinfo'),

]