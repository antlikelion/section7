from rest_framework.response import Response
from rest_framework.views import APIView
from users.api.serializers import UserDisplaySerializer


class CurrentUserAPIView(APIView):
    # 클래스 기반 뷰 1단계 

    def get(self, request):
        # handler method
        serializer = UserDisplaySerializer(request.user)
        return Response(serializer.data)
