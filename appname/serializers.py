from rest_framework.serializers import ModelSerializer
from .models import KayipUser,Ihbar


class IhbarSerializer(ModelSerializer):
    class Meta:
        model = Ihbar
        fields = "__all__"

class KayipUserSerializer(ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:

            ihbar_instance = Ihbar.objects.filter(kayip_user=instance.id).first()
            data['ihbarci_name']=ihbar_instance.ihbar_user.ihbar_first_name
            data['ihbarci_last_name']=ihbar_instance.ihbar_user.ihbar_last_name
            data['ihbarci_phone']=ihbar_instance.ihbar_user.phonenumber

        except Exception as err:
            print(err,'some rrorkerr')
        return data

    class Meta:
        model = KayipUser
        fields = "__all__"