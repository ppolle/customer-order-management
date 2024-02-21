from django.urls import path, include
from rest_framework.routers import DefaultRouter
from savannah.apps.customers.api.viewsets import CustomerViewsets

router = DefaultRouter()
router.register("customers", CustomerViewsets, basename="customers")

urlpatterns = [
    path("", include(router.urls)),
]
