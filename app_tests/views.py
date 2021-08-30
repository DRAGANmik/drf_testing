from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet


from .models import Test
from .serializers import ResultPostSerializer, TestSerializer


class ListRetrieveViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    pass


class TestViewSet(ListRetrieveViewSet):
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
        """
        Endpoint for answer selected test.
         "questions' field must contains all answers for current test.
         """

        serializer = self.serializer_class(
            data=request.data,
            context={"request": request, "test_pk": pk},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
