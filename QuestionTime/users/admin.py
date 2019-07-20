from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    # add_form = UserCreationForm
    # form = UserChangForm
    # 아마 admin페이지에서 user모델을 add하고 변경하는 form양식인 것 같긴한데 
    # form을 직접 만들어줘야되나 봄

    # 문제는 그냥 admin.site.register(CustomUser)해도 잘 됨. 
    # 우리 프로젝트에는 일단 위처럼 push해놨는데 커스텀하는 것도 나쁘지 않을 듯.
    model = CustomUser
    list_display = ["username", "email", "is_staff"]
    # user모델에 등록된 필드가 굉장히 많기 때문에 꼭 필요한 것만 보여주기 위함


admin.site.register(CustomUser, CustomUserAdmin)
