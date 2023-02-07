from django.shortcuts import render, redirect
from .forms import KayipUserForm,IhbarUserForm
from .models import Ihbar,KayipUser,Tag,TagArabic
from django.db import IntegrityError, transaction
from django.core.serializers import json
from django.core.serializers import serialize
from .serializers import KayipUserSerializer
from rest_framework.generics import ListAPIView

import json
import itertools



def IhbarView(request):
    tags = Tag.objects.all()
    kayipuserform = KayipUserForm()
    ihbaruserform = IhbarUserForm()
    if request.method == "POST":
        kayip_first_name = (request.POST.getlist('kayip_first_name',[]))
        kayip_last_name = (request.POST.getlist('kayip_last_name',[]))
        kayip_phone_number = (request.POST.getlist('kayip_phone_number',[]))
        cordinate_x = request.POST.get('cordinate_x',None)
        cordinate_y = request.POST.get('cordinate_y',None)
        address = request.POST.get('address',None)
        kayip_tags = []
        kayip_tags.append((request.POST.getlist('tags',[])))

        print(request.POST,'kayipdass')


        matched_infos =  list(itertools.zip_longest(kayip_first_name,kayip_last_name,kayip_phone_number,kayip_tags))

        # matched_infos = zip(kayip_first_name,kayip_last_name,kayip_phone_number,kayip_tags)

        print(matched_infos,'matchedinfos')

        kayipuserform = KayipUserForm(request.POST)
        ihbaruserform = IhbarUserForm(request.POST)

        if(ihbaruserform.is_valid() and kayipuserform.is_valid()):

                try:
                    with transaction.atomic():
                        ihbarform_instance=ihbaruserform.save()
                        
                        # kayip_form_instance=kayipuserform.save()
                        saved_records = []
                        # saved_records.append(kayip_form_instance.id)
                        for index,(first_name,last_name,phone_number,tag) in enumerate(list(matched_infos)):
                            print(first_name,last_name,phone_number,tag,'matchkkk')
                       
                            kayip_user_instance = KayipUser.objects.create(
                                kayip_first_name = first_name,
                                kayip_last_name = last_name,
                                kayip_phone_number = phone_number,
                                cordinate_x=cordinate_x,
                                cordinate_y=cordinate_y,
                                address=address,

                            )
                            if(tag):
                                tag_arr = [int(x) for x in tag]
                                kayip_user_instance.tags.add(*tag_arr)
                            kayip_user_instance.save()
                            saved_records.append(kayip_user_instance.id)



                        ihbar_instance = Ihbar.objects.create()
                        ihbar_instance.ihbar_user = ihbarform_instance
                        ihbar_instance.kayip_user.add(*saved_records)

                        ihbar_instance.save()
                        # return redirect('ihbarview_tr')
                

                except Exception as err:
                    print(err,'errrr')
        else:
            print(ihbaruserform.errors,'ihbarformerros')
            print(kayipuserform.errors,'kayipuserform')



    return render(request,"ihbar.html",{"kayipuserform":kayipuserform,"ihbaruserform":ihbaruserform,"tags":tags})


def IhbarViewAR(request):
    tags = TagArabic.objects.all()
    kayipuserform = KayipUserForm()
    ihbaruserform = IhbarUserForm()
    if request.method == "POST":
        kayip_first_name = (request.POST.getlist('kayip_first_name',[]))
        kayip_last_name = (request.POST.getlist('kayip_last_name',[]))
        kayip_phone_number = (request.POST.getlist('kayip_phone_number',[]))
        # kayip_tags = (request.POST.getlist('tags',[]))

        matched_infos = zip(kayip_first_name,kayip_last_name,kayip_phone_number)

        kayipuserform = KayipUserForm(request.POST)
        ihbaruserform = IhbarUserForm(request.POST)
        print(request.POST,'requestpossst')
        if(ihbaruserform.is_valid() and kayipuserform.is_valid()):

                try:
                    with transaction.atomic():
                        ihbarform_instance=ihbaruserform.save()
                        
                        kayip_form_instance=kayipuserform.save()

                        for first_name,last_name,phone_number in matched_infos:
                            kayip_user_instance = KayipUser.objects.create(
                                kayip_first_name = first_name,
                                kayip_last_name = last_name,
                                kayip_phone_number = phone_number,
                                cordinate_x=kayip_form_instance.cordinate_x,
                                cordinate_y=kayip_form_instance.cordinate_y,
                                address=kayip_form_instance.address,
                            )
                            ihbar_instance = Ihbar.objects.create()
                            ihbar_instance.ihbar_user = ihbarform_instance
                            ihbar_instance.kayip_user.add(kayip_user_instance)
                            ihbar_instance.save()

                        ihbar_instance = Ihbar.objects.create()
                        ihbar_instance.ihbar_user = ihbarform_instance
                        ihbar_instance.kayip_user.add(kayip_form_instance)
                        ihbar_instance.save()
                        return redirect('ihbarview_ar')
                

                except IntegrityError:
                    raise IntegrityError('Check the values that you sent !')
        else:
            print(ihbaruserform.errors,'ihbarformerros')
            print(kayipuserform.errors,'kayipuserform')


    return render(request,"ihbar_arabic.html",{"kayipuserform":kayipuserform,"ihbaruserform":ihbaruserform,"tags":tags})




def KayipUserList(request):
    users = KayipUser.objects.order_by('-id')
    return render(request,'user_list.html',{"users":str(users.values())})

def KayipUserListAR(request):
    users = KayipUser.objects.order_by('-id')
    return render(request,'user_list_ar.html',{"users":str(users.values())})



class KayipUserListView(ListAPIView):
    queryset = KayipUser.objects.order_by('-id')
    serializer_class = KayipUserSerializer
