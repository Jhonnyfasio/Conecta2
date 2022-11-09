from gestionUsuarios.viewsets import userviewsets
from gestionUsuarios.views import SuggestionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('suggestion', SuggestionViewSet, basename='suggestionset')
urlpatterns = router.urls