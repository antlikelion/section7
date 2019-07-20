"""QuestionTime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from django_registration.backends.one_step.views import RegistrationView
# https://django-registration.readthedocs.io/en/2.1/custom-user.html
# from registration.backends.hmac.views import RegistrationView
# 위 문서에 나온 것과는 조금 다르긴 한데 어쨌든 user모델을 custom한 경우 설정해줘야 함

from core.views import IndexTemplateView

from users.forms import CustomUserForm
# 밑에 url을 보면 view에서 활용함


# https://django-registration.readthedocs.io/en/3.0/activation-workflow.html

urlpatterns = [
    path('admin/', admin.site.urls),

    path("accounts/register/",
         RegistrationView.as_view(
             form_class=CustomUserForm,
             success_url="/",
             ), name="django_registration_register"), 

    path("accounts/",
         include("django_registration.backends.one_step.urls")),
    # 밑의 url pattern을 오버라이드?하는 모양임

    path("accounts/", include("django.contrib.auth.urls")),
    # 장고의 계정 관련된 기본 엔드포인트? 제공 

    path("api/", include("users.api.urls")),
    path("api/", include("questions.api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/rest-auth/", include("rest_auth.urls")),        
    path("api/rest-auth/registration/", include("rest_auth.registration.urls")),

    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")
    # ^는 문자열의 시작을 알림
    # .는 모든 문자를 가리킴
    # * means "any number of this"
    # 따라서 .*는 길이의 제한이 없는 임의의 문자열
    # $는 문자열의 끝을 알림
    # 결론적으로 ^.*$은 문자열의 시작과 끝 사이에 길이의 제한이 없는 임의의 문자열이 온다는 것을 의미
    
    # SPA를 위해서 하는 것 같긴 함... 유데미 재생이 안 되서 확인을 못 함
]
