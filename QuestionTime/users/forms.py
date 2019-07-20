from django_registration.forms import RegistrationForm
# https://django-registration.readthedocs.io/en/2.1/custom-user.html
# RegistrationForm은 장고에 내장된 UserCreationForm의 subclass이다.
# (UserCreationForm은 django.contrib.auth.models.User을 모델로 하는 ModelForm이다)
# UserCreationForm과의 다른 점은 email필드 값을 요구하며, ReversedNameValidator를 적용한다는 것이다.
# 결국 이 Form을 적용하면 회원가입시 인증해달라고 메일이 오는 것
# *custom한 user모델에 django-registration을 적용하려면 필요하다고 함(우리 프로젝트에도...?) 

from users.models import CustomUser

class CustomUserForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = CustomUser
