from django.contrib.auth.models import AbstractUser
# setting.py에 INSTALLED_APPS에 'django.contrib.auth' 설치되어 있음
# 'django.contrib.auth' : 인증관련 기본 변수를 정의함
# User 모델과 Permission 모델, 그리고 Group 모델을 가지고 있음


class CustomUser(AbstractUser):
    pass
    # AbstractUser는 결국 기본 user모델을 커스텀하기 위해서 쓰는 기능

# 처음으로 makemigrations나 migrate을 하기 전에 settings.py에 
# AUTH_USER_MODEL = "users.CustomUser" 꼭 등록해줘야 함
# 또한 admin.py에도 꼭 등록을 해줘야 한다고 함(선택사항이 아닌가 봄)

