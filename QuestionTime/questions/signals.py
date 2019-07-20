from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
# 1.allow_unicode값을 True로 주지 않는 한 디폴트는 False이고 이 상태에선 ASCII로 변환한다
# 2.(문자,숫자,_,-,공백)이 아닌 character는 제거한다.
# 3.앞의 공백과 뒤의 공백을 제거한다.
# 4.소문자로 변환한다.
# 5.모든 공백과 반복된-를 하나의-로 바꾼다.
# 위의 과정을 거쳐 문자열을 URL slug로 변환한다.

from core.utils import generate_random_string
from questions.models import Question

@receiver(pre_save, sender=Question)
def add_slug_to_question(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        # 객체는 존재하지만 객체의 슬러그는 존재하지 않는 상태를 의미하는 듯?
        slug = slugify(instance.content)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string