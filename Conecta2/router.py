from gestionUsuarios.viewsets import userviewsets
from gestionUsuarios.views import SuggestionViewSet
from api.views import CardPostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'suggestion', SuggestionViewSet, basename='suggestionset')
urlpatterns = router.urls