from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/', views.PetCreateView.as_view(), name='new'),
    # url(r'^$', views.ProductListView.as_view(), name='list'),
]