from django import forms
from .models import IhbarUser,KayipUser,Ihbar

class IhbarUserForm(forms.ModelForm):
    class Meta:
        model = IhbarUser
        fields = "__all__"

class KayipUserForm(forms.ModelForm):
    class Meta:
        model = KayipUser
        exclude = ["cordinate_x","cordinate_y"]


class IhbarForm(forms.ModelForm):
    class Meta:
        model = Ihbar
        fields = "__all__"