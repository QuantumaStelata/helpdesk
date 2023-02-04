from rest_framework import routers

from .views import FieldViewSet, NodeViewSet


app_name = "api"

router = routers.DefaultRouter()
router.register(r'fields', FieldViewSet)
router.register(r'nodes', NodeViewSet)

urlpatterns = router.urls
