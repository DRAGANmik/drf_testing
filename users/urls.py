from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RegisterApiView, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    # path("users/", UserApiView.as_view(), name="users"),
    path("register/", RegisterApiView.as_view(), name="register"),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include(router.urls)),
]
