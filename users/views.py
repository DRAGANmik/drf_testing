from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from .serializers import UserDetailSerializer, UserRegisterSerializer

User = get_user_model()


class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        url_path="me",
        url_name="me",
    )
    def view_me(self, request):
        """ """
        if request.user.id:
            serializer = UserDetailSerializer(request.user, data=request.data)

            if serializer.is_valid() and request.method == "PATCH":
                serializer.save()
            serializer = UserDetailSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
