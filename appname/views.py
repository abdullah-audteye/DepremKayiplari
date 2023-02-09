from django.shortcuts import render, redirect
from .forms import KayipUserForm, IhbarUserForm
from .models import Ihbar, KayipUser, Tag, Countries, KayipStatus,IhbarUser
from django.db import transaction
from django.http import JsonResponse
from django.http import QueryDict
from .serializers import KayipUserSerializer, IhbarSerializer, KayipStatusSerializer
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from .helper import CleanBadRecords,FixNonHavingDates
from datetime import datetime
import random

def ChangeKayipStatus(request,pk):
    ihbar = get_object_or_404(Ihbar,pk=pk)
    kayip_status = KayipStatus.objects.all()
    return render(request,'change_status.html',{"ihbar":ihbar,'kayip_status':kayip_status})



def IhbarView(request):
    tags = Tag.objects.all()
    countries = Countries.objects.all()
    kayipstatus = KayipStatus.objects.all()

    kayipuserform = KayipUserForm()
    ihbaruserform = IhbarUserForm()
    if request.method == "POST":
        kayip_user_data = (request.POST.getlist('data[]'))
        ihbarci_data = QueryDict(request.POST.get('ihbarci_data'))
        ihbaruserform = IhbarUserForm(ihbarci_data)

        if ihbaruserform.is_valid():
            cordinate_x = ihbarci_data.get('cordinate_x')
            cordinate_y = ihbarci_data.get('cordinate_y')
            record_status = True

            try:
                with transaction.atomic():
                    ihbaruserform_instance = ihbaruserform.save()

                    saved_records = []
                    for kayip_user in kayip_user_data:
                        kayip_user = QueryDict(kayip_user).copy()
                        kayip_user['cordinate_x'] = cordinate_x
                        kayip_user['cordinate_y'] = cordinate_y

                        kayip_user_check = KayipUserForm(kayip_user)
                        if (kayip_user_check.is_valid()):
                            kayip_user_instance = kayip_user_check.save()

                            saved_records.append(kayip_user_instance.id)
                        else:
                            record_status = False
                            IhbarUser.objects.get(id=ihbaruserform_instance.id).delete()




                    if record_status:
                        ihbar_instance = Ihbar.objects.create()
                        access_number = random.randint(000000,999999)

                        ihbar_instance.ihbar_user = ihbaruserform_instance
                        ihbar_instance.access_code = access_number
                        ihbar_instance.kayip_user.add(*saved_records)
                        ihbar_instance.created_time = datetime.now()
                        ihbar_instance.save()
                        CleanBadRecords()
                        FixNonHavingDates()
                        return JsonResponse({'status': True, 'message': "success"}, status=200)

                    else:
                        return JsonResponse({'status': False, 'message': "Failed"}, status=200)



            except Exception as err:
                print(err, 'errrr')

    return render(request, "ihbar.html",
                  {"kayipuserform": kayipuserform, "ihbaruserform": ihbaruserform, "tags": tags, "countries": countries,
                   "kayip_status": kayipstatus})



def IframeForm(request):
    return render(request,'iframeform.html')


def IframeDashboard(request):
    return render(request,'iframeform.html')



class KayipUserListView(ListAPIView):
    queryset = Ihbar.objects.order_by('-id')
    serializer_class = IhbarSerializer


class KayipStatusListView(ListAPIView):
    queryset = KayipStatus.objects.all()
    serializer_class = KayipStatusSerializer


