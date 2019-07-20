from django.db import models
from django.conf import settings


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True값을 지정해주면 해당 필드는 객체가 처음 생성되었을 때를 기록한다.
    updated_at = models.DateTimeField(auto_now=True)
    # auto_now=True값을 지정해주면 해당 필드는 Model.save()가 호출될 때만 갱신된다.
    content = models.CharField(max_length=240)
    slug = models.SlugField(max_length=255, unique=True)
    # 슬러그는 신문용어라고 함 
    # 보통 url에서 쓰이는 (문자,숫자,_,-)로만 이루어진 짧은 라벨임
    # max_length를 지정해주지 않으면 디폴트 값으로 50의 길이만 할당함
    # Field.db_index=True를 함축하고 있음(db_index값을 매긴다는 의미)
    # admin에서 prepopulated_fields를 사용하여 자동으로 slugfield를 생성하는 방법이 있는데
    # 이 튜토리얼에서는 그냥 시그널 활용
    # unique=True면 테이블에 이 필드가 하나만 존재해야 함
    # -> Question모델에 SlugField가 하나만 있어야 된다는 의미로 이해했는데 맞는지 모르겠음
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="questions")
    # 여기서 settings.AUTH_USER_MODEL대신에 CustomUser모델을 직접 import해와서 쓰면 안 됨.
    # 유저 모델을 커스텀했을 때 준수해야할 사항임

    def __str__(self):
        return self.content


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True값을 지정해주면 해당 필드는 객체가 처음 생성되었을 때를 기록한다.
    updated_at = models.DateTimeField(auto_now=True)
    # auto_now=True값을 지정해주면 해당 필드는 Model.save()가 호출될 때만 갱신된다.
    body = models.TextField()
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name="answers")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name="votes")
    # ForeignKey가 recursive하고 lazy한 관계를 갖춘 형태이다.
    # recursive는 말그대로 재귀임 자기자신과 엮는 것
    # lazy는 다른 앱에 정의된 모델을 앱이름.모델이름 과 같은 방식으로 가리키는 것인데
    # 이러면 서로가 서로를 import하는 순환 문제를 해결할 수 있다.

    def __str__(self):
        return self.author.username