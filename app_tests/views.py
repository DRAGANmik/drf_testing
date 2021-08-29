from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Test
from .serializers import ResultPostSerializer, TestSerializer


class TestViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    @action(
        detail=True,
        methods=["POST"],
        url_path="answer",
        url_name="test-answer",
        serializer_class=ResultPostSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def test_answer(self, request, pk):
        """ """

        serializer = self.serializer_class(
            data=request.data,
            context={"request": request, "test_pk": pk},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
