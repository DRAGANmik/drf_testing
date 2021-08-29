from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField(
        "Question", through="QuestionItem", through_fields=("test", "question")
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    question = models.TextField()
    answers = models.ManyToManyField(
        "Answer", related_name="answers", blank=True
    )

    def __str__(self):
        return self.question


class QuestionItem(models.Model):
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="app_tests"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="Чтобы добавить ответы, нажмите редактировать",
    )

    def __str__(self):
        return "Тест: {} - вопрос: {}".format(self.test, self.question)


class Answer(models.Model):
    answer = models.TextField()
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(
            self.answer, '"Правильный"' if self.correct_answer else ""
        )


class Result(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="results"
    )

    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "test"], name="unique_result"
            )
        ]


class ResultItem(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    question_item = models.ForeignKey(QuestionItem, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return "Пользователь: {} - вопрос id: {} - ответ: {}".format(
            self.result.user, self.question_item.id, self.answer
        )
