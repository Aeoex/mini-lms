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
    
    def update(self, instance, validated_data):
        """Allow updating nested questions and choices."""
        questions_data = validated_data.pop("questions", None)
        lesson = validated_data.pop("lesson", None)

        # Update quiz fields directly
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update lesson if changed
        if lesson and lesson.quiz != instance:
            lesson.quiz = instance
            lesson.save(update_fields=["quiz"])

        # Handle nested question updates
        if questions_data is not None:
            # Remove old questions not included in update
            existing_question_ids = [q.id for q in instance.questions.all()]
            new_question_ids = [q.get("id") for q in questions_data if q.get("id")]
            to_delete = set(existing_question_ids) - set(new_question_ids)
            Question.objects.filter(id__in=to_delete).delete()

            # Create or update questions
            for question_data in questions_data:
                choices_data = question_data.pop("choices", [])
                question_id = question_data.pop("id", None)

                if question_id:
                    # Update existing question
                    question = Question.objects.get(id=question_id, quiz=instance)
                    for attr, value in question_data.items():
                        setattr(question, attr, value)
                    question.save()
                else:
                    # Create new question
                    question = Question.objects.create(quiz=instance, **question_data)

                # Handle choices for this question
                existing_choice_ids = [c.id for c in question.choices.all()]
                new_choice_ids = [c.get("id") for c in choices_data if c.get("id")]
                to_delete_choices = set(existing_choice_ids) - set(new_choice_ids)
                Choice.objects.filter(id__in=to_delete_choices).delete()

                for choice_data in choices_data:
                    choice_id = choice_data.pop("id", None)
                    if choice_id:
                        choice = Choice.objects.get(id=choice_id, question=question)
                        for attr, value in choice_data.items():
                            setattr(choice, attr, value)
                        choice.save()
                    else:
                        Choice.objects.create(question=question, **choice_data)

        return instance

class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(many=False, required=True)
    enrollment = serializers.PrimaryKeyRelatedField(queryset=Enrollment.objects.all())
    class Meta:
        model = QuizAttempt
        fields = ["id", "quiz", "enrollment", "score", "taken_at"]
        read_only_fields = ["id", "quiz", "enrollment", "score", "taken_at"]
