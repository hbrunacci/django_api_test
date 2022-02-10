from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProductView

router = DefaultRouter()
router.register(r'product', ProductView, basename='product')

urlpatterns = [
    path('', include(router.urls))
]