from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
# 함수 기반 뷰에서 login_required데코레이터를 쓰는 반면,
# 클래스 기반 뷰에서는 LoginRequiredMixin을 상속합니다.
# 상속할 때는 아래와 같이 가장 왼쪽에 상속해줘야 합니다.

from django.views.generic.base import TemplateView
# URL에서 캡쳐한 파라미터를 담고 있는 context와 함께 주어진 template을 반환하는 함수
# 여기서는 context없이 template_name만 반환하는 걸로 커스텀한 모양....
# context는 view에 제공된 'url 패턴에서 캡쳐된 keyword arguments'로 생성된다.
# path('blog/<int:year>/', views.year_archive, {'foo': 'bar'}),
# 여기서 저 딕셔너리 부분이 path함수를 통해 전달하는 kwargs인데 저걸 캡쳐해서 context를 생성하나봄

class IndexTemplateView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        if settings.DEBUG:
            template_name = "index-dev.html"
        else:
        # 배포할 때는 DEBUG값을 True외의 값으로 해야되는 것으로 알고있음
            template_name = "index.html"
        return template_name