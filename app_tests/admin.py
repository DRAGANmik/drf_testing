from django.contrib import admin

from .models import Answer, Question, QuestionItem, Result, ResultItem, Test


class AnswerAdmin(admin.StackedInline):
    # model = Answer.answers.through
    model = Question.answers.through
    extra = 0


class QuestionItemAdmin(admin.StackedInline):
    model = QuestionItem
    extra = 0


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionItemAdmin]


class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerAdmin,)

    fields = [
        "question",
    ]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()

        return super().get_inline_instances(request, obj)


class ResultAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "test", "stats"]

    def stats(self, obj):
        correct_answer = obj.resultitem_set.filter(
            answer__correct_answer=True
        ).count()
        ratio = round(correct_answer * 100 / obj.resultitem_set.count(), 2)
        return str(ratio) + " %"


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionItem)
admin.site.register(Answer)
admin.site.register(Result, ResultAdmin)
admin.site.register(ResultItem)
