from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from pets import views as p


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('rest_framework.urls')),
    url(r'^pets/', include('pets.urls')),
    url(r'^api/users/$', p.UserList.as_view()),
    url(r'^api/users/(?P<pk>\d+)$', p.UserDetail.as_view()),


]
