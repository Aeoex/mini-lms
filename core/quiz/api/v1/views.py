from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, generics

from ...models import Quiz, Question, Choice, QuizAttempt
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, QuizAttemptSerializer
from enrollment.models import Enrollment


class QuizModelViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="submit")
    def submit_quiz(self, request, pk=None):
        quiz = self.get_object()
        answers = request.data.get("answers", [])

        correct = 0
        total = quiz.questions.count()

        for answer in answers:
            try:
                choice = Choice.objects.get(
                    id=answer["choice_id"],
                    question_id=answer["question_id"]
                )
                if choice.is_correct:
                    correct += 1
            except Choice.DoesNotExist:
                pass

        score = int((correct / total) * 100) if total > 0 else 0

        enrollment = Enrollment.objects.get(user_profile__user=request.user, course = quiz.lesson.course)
        QuizAttempt.objects.create(
            quiz=quiz,
            enrollment=enrollment,
            score=score
        )

        return Response(
            {"score": score, "correct_answers": correct, "total_questions": total},
            status=status.HTTP_200_OK
        )


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        quiz_id = self.request.data.get("quiz")
        serializer.save(quiz_id=quiz_id)


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        question_id = self.request.data.get("question")
        serializer.save(question_id=question_id)



class QuizAttemptListAPIView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]
    queryset = QuizAttempt.objects.all()

    def get_queryset(self):
        return QuizAttempt.objects.filter(enrollment__user_profile__user=self.request.user)
    

class QuizAttemptRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]
    queryset = QuizAttempt.objects.all()

    def get_queryset(self):
        return QuizAttempt.objects.filter(enrollment__user_profile__user=self.request.user)