from django.urls import include, path

from .views import RegisterApiView, UserApiView

urlpatterns = [
    path("users/", UserApiView.as_view(), name="users"),
    path("register/", RegisterApiView.as_view(), name="register"),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
