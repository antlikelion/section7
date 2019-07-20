from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# 클라이언트의 요청에 따라 다양한 타입으로 렌더링 가능한 컨텐트를 반환하는 클래스
# response 객체를 반환하기 위해서 APIView를 상속하던지 @api_view데코레이터를 사용하던지 해야한다.
from rest_framework.views import APIView

from questions.api.permissions import IsAuthorOrReadOnly
from questions.api.serializers import AnswerSerializer, QuestionSerializer
from questions.models import Answer, Question


class AnswerCreateAPIView(generics.CreateAPIView):
    """Allow users to answer a question instance if they haven't already."""
    queryset = Answer.objects.all()
    # 하나만 만드는 건데 def get_object()로 커스텀하면 안 될 이유가 있나...
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 새로운 객체 인스턴스를 저장할 때 CreateModelMixin이 호출하는 함수
        # 굳이 이걸 커스텀하는 이유는 request에 내포되어 있지만 request data의 일부가 아닌
        # 속성을 설정하는 데 유용하기 때문이라고 함
        request_user = self.request.user
        # Answer모델의 author가 가리키는 유저값을 특정해주기 위함
        # Answer에 request_user라는 필드는 없으니 AnswerCreateAPIView가
        # author에 저장할 값을 자동으로 인식하지 못하기 때문에 이렇게 하는 것 같음
        kwarg_slug = self.kwargs.get("slug")
        # url을 보면 path converter에도 slug가 있고, 바로 그 뒤에도 slug가 있음 
        # 뭘 참조하는 건지는 모르겠다만...
        # self가 request url이라고 가정하면 kwargs의 key값 slug에 대응하는 value값을 반환
        question = get_object_or_404(Question, slug=kwarg_slug)
        # Question모델에서 slug를 기준으로 객체를 찾아서 있으면 반환하고 없으면 404오류 반환
        # Answer에 관한 뷰에서 Question이 필요하니 커스텀함수가 필요한 것
        # questions url 하위에 answers url이 있음을 염두에 둬야 한다
        if question.answers.filter(author=request_user).exists():
            # question에서 자식 모델인 answer를 참조하기 위해 related name을 참조함
            raise ValidationError("You have already answered this Question!")

        serializer.save(author=request_user, question=question)


class AnswerLikeAPIView(APIView):
    """Allow users to add/remove a like to/from an answer instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """Remove request.user from the voters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """Add request.user to the voters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.voters.add(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerListAPIView(generics.ListAPIView):
    """Provide the answers queryset of a specific question instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answer.objects.filter(question__slug=kwarg_slug).order_by("-created_at")
        # 최근에 만들어진 순으로 정렬
        # 밑줄 두 개 끄은 건 무슨 원리인지...


class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Provide *RUD functionality for an answer instance to it's author."""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    """Provide CRUD +L functionality for Question."""
    queryset = Question.objects.all().order_by("-created_at")
    lookup_field = "slug"
    # https://www.django-rest-framework.org/api-guide/generic-views/#attributes
    # GenericAPIView의 속성 중 하나로 디폴트 값은 pk이다.
    # 말그대로 찾을 필드이다. 
    # url에서 찾고자 하면 lookup_url_kwarg를 쓰면 되는데
    # lookup_url_kwarg를 설정 안 했을 경우 lookup_field와 동일한 값을 사용한다.

    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # 역시나 관계를 명확히 지정해주기 위한 커스텀이다
        serializer.save(author=self.request.user)

    