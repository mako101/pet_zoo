from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^new/', views.GuiPetCreateView.as_view(), name='new'),
    # url(r'^my-pets/', views.GuiPetListView.as_view(), name='my_pets'),
    # url(r'^api/$', views.pet_list),
    # url(r'^api/(?P<pk>\d+)$', views.pet_detail)
    url(r'^$', views.PetList.as_view(), name='pet-list'),
    url(r'^(?P<pk>\d+)$', views.PetDetail.as_view(), name='pet-detail')
]
