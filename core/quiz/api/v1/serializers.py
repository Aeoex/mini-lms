from django.utils import timezone
from rest_framework import serializers
from ...models import Quiz, Question, Choice, QuizAttempt
from course.models import Lesson
from enrollment.models import Enrollment




class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "content", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ["id", "content", "choices"]

    def create(self, validated_data):
        choices_data = validated_data.pop("choices", [])
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=True)
    lesson = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(),
        allow_null=False,
        required=True,
    )
    lesson_title = serializers.CharField(
        source = "lesson.title",
        read_only = True
    )

    class Meta:
        model = Quiz
        fields = ["id", "questions", "lesson", "lesson_title"]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        lesson = validated_data.pop("lesson", None)
        if lesson :
            quiz = Quiz.objects.create(**validated_data)
            lesson.quiz = quiz
            lesson.save(update_fields=["quiz"])
            for question_data in questions_data:
                choices_data = question_data.pop("choices", [])
                question = Question.objects.create(quiz=quiz, **question_data)
                for choice_data in choices_data:
                    Choice.objects.create(question=question, **choice_data)
            return quiz

class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(many=False, required=True)
    enrollment = serializers.PrimaryKeyRelatedField(queryset=Enrollment.objects.all())
    class Meta:
        model = QuizAttempt
        fields = ["id", "quiz", "enrollment", "score", "taken_at"]
        read_only_fields = ["id", "quiz", "enrollment", "score", "taken_at"]
