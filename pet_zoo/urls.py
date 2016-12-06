from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from pets import views as p


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/users', p.UserViewSet)
router.register(r'api/pets', p.PetViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/$', p.api_root),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/species/$', p.SpeciesList.as_view(), name='species-list'),
    url(r'^api/species/(?P<pk>\d+)$', p.SpeciesDetail.as_view(), name='species-detail'),
    # url(r'^api/users/$', p.UserList.as_view(), name='user-list'),
    # url(r'^api/users/(?P<pk>\d+)$', p.UserDetail.as_view(), name='user-detail'),
    # url(r'^api/pets/', include('pets.urls')),

]
