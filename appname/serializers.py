from rest_framework.serializers import ModelSerializer
from .models import KayipUser
class KayipUserSerializer(ModelSerializer):
    class Meta:
        model = KayipUser
        fields = "__all__"