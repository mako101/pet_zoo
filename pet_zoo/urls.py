from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from pets import views as p


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', p.UserViewSet)
router.register(r'pets', p.PetViewSet)
router.register(r'species', p.SpeciesViewSet)

urlpatterns = [

    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
]
