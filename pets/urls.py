from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/', views.PetCreateView.as_view(), name='new'),
    url(r'^my-pets/', views.PetListView.as_view(), name='my_pets'),
]