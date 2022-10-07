from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()

router.register('v1/post', PostViewSet)


urlpatterns = router.urls

