from django.urls import path, include
from rest_framework.routers import DefaultRouter
from savannah.apps.orders.api.viewsets import OrderViewSets

router = DefaultRouter()
router.register("orders", OrderViewSets, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
