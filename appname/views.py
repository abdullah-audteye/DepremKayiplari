from django.shortcuts import render, redirect

# from appname.models import User
from .forms import IhbarForm,KayipUserForm,IhbarUserForm


def IhbarView(request):
    ihbarform = IhbarForm()
    kayipuserform = KayipUserForm()
    ihbaruserform = IhbarUserForm()
    if request.method == "POST":
        ihbarform = IhbarForm(request.POST)
        if ihbarform.is_valid():
            ihbarform.save()
            return redirect('index')
    return render(request,"ihbar.html",{"ihbarform":ihbarform,"kayipuserform":kayipuserform,"ihbaruserform":ihbaruserform})


