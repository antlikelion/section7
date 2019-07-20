from django.urls import include, path
from rest_framework.routers import DefaultRouter
# DefaultRouter는 SimpleRouter의 기능에 더해 모든 list view에 하이퍼링크를 달아서 response를 보내는 Default API root view를 가진다.
# 또한 url주소에 json형태의 접미사가 붙은 route를 생성한다.

from questions.api import views as qv
# question view의 약자인 듯

router = DefaultRouter()
router.register(r"questions", qv.QuestionViewSet)
# url패턴 : ^questions/$ url이름 : question-list
# url패턴 : ^questions/{slug:slug}/$ url이름 : question-detail

urlpatterns = [
    path("", include(router.urls)),

    path("questions/<slug:slug>/answers/",
         qv.AnswerListAPIView.as_view(),
         name="answer-list"),

    path("questions/<slug:slug>/answer/",
         qv.AnswerCreateAPIView.as_view(),
         name="answer-create"),

    path("answers/<int:pk>/",
         qv.AnswerRUDAPIView.as_view(),
         name="answer-detail"),

    path("answers/<int:pk>/like/",
         qv.AnswerLikeAPIView.as_view(),
         name="answer-like")
]
