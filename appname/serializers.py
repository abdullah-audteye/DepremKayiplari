from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import KayipUser,Ihbar,IhbarUser,KayipStatus

def PutAsteriskSymbol(value,cut_value=2,phonenumber=False):
    new_first_name = ""
    splitted_names=[]
    if phonenumber == False:
        splitted_names = value.split(' ')
    else:
        splitted_names.append(value)

    
    for i in splitted_names:
        new_first_name+=(i[:cut_value]) + (cut_value) * "**" + " "
    
    return new_first_name



class KayipUserSerializer(ModelSerializer):

    kayip_first_name = SerializerMethodField()
    kayip_last_name = SerializerMethodField()

    def get_kayip_first_name(self,obj):
        return PutAsteriskSymbol(obj.kayip_first_name)
    
    def get_kayip_last_name(self,obj):
        return PutAsteriskSymbol(obj.kayip_last_name)
    


    class Meta:
        model = KayipUser
        fields = "__all__"


class IhbarUserSerializer(ModelSerializer):

    ihbar_first_name = SerializerMethodField()
    ihbar_last_name = SerializerMethodField()
    phonenumber = SerializerMethodField()
    eposta = SerializerMethodField()

    def get_ihbar_first_name(self,obj):
        return PutAsteriskSymbol(obj.ihbar_first_name)
    
    def get_ihbar_last_name(self,obj):
        return PutAsteriskSymbol(obj.ihbar_last_name)
    
    def get_phonenumber(self,obj):
        return PutAsteriskSymbol(obj.phonenumber,3,True)

    def get_eposta(self,obj):
        return PutAsteriskSymbol(obj.eposta,4)

    class Meta:
        model = IhbarUser
        fields = "__all__"

class IhbarSerializer(ModelSerializer):
    ihbar_user = IhbarUserSerializer()
    kayip_user = KayipUserSerializer(many=True)

    

    class Meta:
        model = Ihbar
        exclude = ['access_code']

class KayipStatusSerializer(ModelSerializer):
    class Meta:
        model = KayipStatus
        fields = "__all__"