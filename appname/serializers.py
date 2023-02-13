from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import KayipUser,Ihbar,Cities,IhbarUser,KayipStatus

def PutAsteriskSymbol(value,cut_value=2,phonenumber=False):
    try:
        new_first_name = ""
        splitted_names=[]
        if phonenumber == False and value:
            splitted_names = value.split(' ')
        else:
            splitted_names.append(value)

        
        for i in splitted_names:
            new_first_name+=(i[:cut_value]) + (cut_value) * "**" + " "
        
        return new_first_name
    except:
        return value



class KayipUserSerializer(ModelSerializer):

    kayip_first_name = SerializerMethodField(read_only=True)
    kayip_last_name = SerializerMethodField(read_only=True)

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


class ReporterUserSerializer(ModelSerializer):
    class Meta:
        model = IhbarUser
        fields = "__all__"

class ReportedUserSerializer(ModelSerializer):
    class Meta:
        model = KayipUser
        fields = "__all__"

class CitiesSerializer(ModelSerializer):
    class Meta:
        model = Cities
        fields = "__all__"

class ReportSerializer(ModelSerializer):
    kayip_user = ReportedUserSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ihbar_user_name'] = instance.ihbar_user.ihbar_first_name + " " + instance.ihbar_user.ihbar_last_name
        data['ihbar_user_phone_number'] = instance.ihbar_user.phonenumber
        return data

    class Meta:
        model = Ihbar
        exclude = ['access_code']


class KayipStatusSerializer(ModelSerializer):
    class Meta:
        model = KayipStatus
        fields = "__all__"