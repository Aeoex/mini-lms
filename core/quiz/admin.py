from django.contrib import admin


from .models import Question, Quiz, Choice, QuizAttempt
# Register your models here.

admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Choice)
admin.site.register(QuizAttempt)