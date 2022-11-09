from api.views import CardPostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cardset/', CardPostViewSet, basename='cardset')
urlpatterns = router.urls