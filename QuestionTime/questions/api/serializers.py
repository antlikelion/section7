from rest_framework import serializers
from questions.models import Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    # 지환이가 얘기한것처럼 model에 __str__메소드가 있어야 함
    # ModelSerializer 유의사항? : 모델에서의 foreignkey와 같은 관계는 PrimaryKeyRelatedField로 변환됨
    # 따로 serializers.py에서 관계를 명시적으로 지정해주지 않으면 역방향의 관계는 포함되지 않는다
    # ->부모모델의 시리얼라이저가 모델시리얼라이저나 하이퍼링크드모델시리얼라이저를 상속한다면
    # 역방향의 관계는 자동으로 포함되지 않기 때문에 부모모델의 시리얼라이저의 메타 클래스의 필드에 
    # 관계 필드의 related_name값을 명시해줘야 한다.
    created_at = serializers.SerializerMethodField()
    # 읽기 전용 필드임
    # 해당 시리얼라이저 클래스의 메소드를 호출함으로써 값을 가지게 됨.
    # SerializerMethodField(method_name=None)과 같이 쓰지 않으면 디폴트 값으로
    # method_name은 get_<field_name>을 디폴트 값으로 가지게 된다.
    likes_count = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField()
    question_slug = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        exclude = ["question", "voters", "updated_at"]

    def get_created_at(self, instance):
        # self이외에 직렬화시킬 하나의 인자만을 전달 받을 수 있다.
        return instance.created_at.strftime("%B %d, %Y")
        # 객체의 직렬화된 표현에 포함시키고자 하는 무언가를 반환해야 한다.
        # %B : Locale의 full month name
        # %d : 날짜(10진수)
        # %Y : 세기까지 포함한 연도(10진수) 
        # strftime(format,t)가 기본 형식인데 format은 str형식이어야 하고 t가 없으면,
        # localtime()을 이용한 현재시간이 이용된다.

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        # "request"가 key값으로 context안에 있으면 value를 반환하고 없으면 otherwise를 반환한다?
        # context는 딕셔너리 타입클래스임
        # 여기서 self가정확히 뭐임... self가 url pattern인건가 그래야 context가 존재하는건데
        return instance.voters.filter(pk=request.user.pk).exists()
        # 불린 값을 반환해야 하기 때문에 exists()

    def get_question_slug(self, instance):
        return instance.question.slug


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    # 시리얼라이저의 SlugField는 정규표현식필드(RegexField)를 상속한다.
    # 근데 이걸 굳이 오버라이드할 이유가...?
    answers_count = serializers.SerializerMethodField()
    user_has_answered = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ["updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        return instance.answers.filter(author=request.user).exists()