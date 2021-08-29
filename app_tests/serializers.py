from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Answer, Question, QuestionItem, Result, ResultItem, Test


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class AnswerTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ["correct_answer"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = "__all__"


class QuestionTestSerializer(QuestionSerializer):
    answers = AnswerTestSerializer(many=True)


# class QuestionItemSerializer(serializers.ModelSerializer):
#     question = QuestionSerializer()
#
#     class Meta:
#         model = QuestionItem
#         fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionTestSerializer(many=True)

    class Meta:
        model = Test
        fields = "__all__"


class ResultItemSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(source="question_item.question")

    class Meta:
        model = ResultItem
        fields = ["id", "answer", "question"]


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ["id", "user", "test"]

    def to_representation(self, instance):
        correct_answer = instance.resultitem_set.filter(
            answer__correct_answer=True
        ).count()
        incorrect_answer = instance.resultitem_set.count() - correct_answer
        ratio = round(
            correct_answer * 100 / instance.resultitem_set.count(), 2
        )
        serializer = ResultItemSerializer(
            instance.resultitem_set.all(), many=True
        )
        return {
            "correct_answers": correct_answer,
            "incorrect_answers": incorrect_answer,
            "ratio": f"{ratio} %",
            "questions": serializer.data,
        }


class ResultItemPostSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )
    answer = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all())

    class Meta:
        model = ResultItem
        fields = ["id", "answer", "question"]


class ResultPostSerializer(serializers.Serializer):
    questions = ResultItemPostSerializer(many=True)

    def validate(self, data):
        questions = data.get("questions")
        test_pk = self.context.get("test_pk")
        test = get_object_or_404(Test, pk=test_pk)
        request = self.context.get("request")
        result = Result.objects.filter(user=request.user, test=test)
        for item in questions:
            if item["answer"] not in item["question"].answers.all():
                raise serializers.ValidationError("Некорректный ответ.")
        if result:
            raise serializers.ValidationError("Вы уже проходили этот тест.")
        if test.questions.count() != len(questions):
            raise serializers.ValidationError("Нужно ответить на все вопросы.")
        return data

    def create(self, validated_data):
        questions = validated_data.get("questions")
        test_pk = self.context.get("test_pk")
        request = self.context.get("request")
        test = get_object_or_404(Test, pk=test_pk)
        result = Result.objects.create(user=request.user, test=test)

        items = [
            ResultItem(
                question_item=get_object_or_404(
                    QuestionItem, question=item["question"], test=test
                ),
                result=result,
                answer=get_object_or_404(Answer, id=item["answer"].id),
            )
            for item in questions
        ]

        ResultItem.objects.bulk_create(items)
        return result

    def to_representation(self, instance):
        correct_answer = instance.resultitem_set.filter(
            answer__correct_answer=True
        ).count()
        incorrect_answer = instance.resultitem_set.count() - correct_answer
        ratio = round(
            correct_answer * 100 / instance.resultitem_set.count(), 2
        )

        return {
            "correct_answers": correct_answer,
            "incorrect_answers": incorrect_answer,
            "ratio": f"{ratio} %",
        }
