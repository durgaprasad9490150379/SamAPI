from django.conf.urls import url
from rest_framework import routers
from .views import DomainViewSet

router = routers.SimpleRouter()
router.register(r'',DomainViewSet, basename='domain')
urlpatterns = router.urls

