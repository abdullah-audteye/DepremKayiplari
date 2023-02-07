from django.shortcuts import render, redirect
from .forms import KayipUserForm,IhbarUserForm
from .models import Ihbar,KayipUser,Tag
from django.db import IntegrityError, transaction
from django.core.serializers import json
from django.core.serializers import serialize
from .serializers import KayipUserSerializer
from rest_framework.generics import ListAPIView

import json



def IhbarView(request):
    tags = Tag.objects.all()
    kayipuserform = KayipUserForm()
    ihbaruserform = IhbarUserForm()
    if request.method == "POST":
        kayipuserform = KayipUserForm(request.POST)
        ihbaruserform = IhbarUserForm(request.POST)

        if(ihbaruserform.is_valid() and kayipuserform.is_valid()):
            try:
                with transaction.atomic():
                    ihbarform_instance=ihbaruserform.save()
                    kayip_form_instance=kayipuserform.save()
                    ihbar_instance = Ihbar.objects.create()
                    ihbar_instance.ihbar_user = ihbarform_instance
                    ihbar_instance.kayip_user.add(kayip_form_instance)
                    ihbar_instance.save()
                    return redirect('ihbarview')
            

            except IntegrityError:
                raise IntegrityError('Check the values that you sent !')
        else:
            print(ihbaruserform.errors,'ihbarformerros')
            print(kayipuserform.errors,'kayipuserform')


    return render(request,"ihbar.html",{"kayipuserform":kayipuserform,"ihbaruserform":ihbaruserform,"tags":tags})


def KayipUserList(request):
    users = KayipUser.objects.order_by('-id')
    return render(request,'user_list.html',{"users":str(users.values())})

class KayipUserListView(ListAPIView):
    queryset = KayipUser.objects.order_by('-id')
    serializer_class = KayipUserSerializer
