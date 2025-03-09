from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from bistro.orders.api.views import MenuViewSet
from bistro.orders.api.views import OrderViewSet
from bistro.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register(r"users", UserViewSet)
router.register(r"menu", MenuViewSet)
router.register(r"orders", OrderViewSet)


app_name = "api"
urlpatterns = router.urls
