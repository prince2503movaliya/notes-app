from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


# 🔐 LOGIN (JWT)
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


# 🔓 LOGOUT (BLACKLIST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    try:
        refresh_token = request.data.get("refresh")

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({
            "success": True,
            "message": "Logged out successfully"
        })

    except Exception:
        return Response({
            "success": False,
            "message": "Invalid token"
        }, status=status.HTTP_400_BAD_REQUEST)