from django.shortcuts import render, redirect
from .forms import KayipUserForm, IhbarUserForm
from .models import Ihbar, KayipUser, Tag, TagArabic, Countries, KayipStatus
from django.db import transaction
from django.http import JsonResponse
from django.http import QueryDict
from .serializers import KayipUserSerializer, IhbarSerializer, KayipStatusSerializer
from rest_framework.generics import ListAPIView


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

                    ihbar_instance = Ihbar.objects.create()
                    ihbar_instance.ihbar_user = ihbaruserform_instance
                    ihbar_instance.kayip_user.add(*saved_records)

                    ihbar_instance.save()
                    return JsonResponse({'status': True, 'message': "success"}, status=200)


            except Exception as err:
                print(err, 'errrr')

    return render(request, "ihbar.html",
                  {"kayipuserform": kayipuserform, "ihbaruserform": ihbaruserform, "tags": tags, "countries": countries,
                   "kayip_status": kayipstatus})


class KayipUserListView(ListAPIView):
    queryset = Ihbar.objects.order_by('-id')
    serializer_class = IhbarSerializer


class KayipStatusListView(ListAPIView):
    queryset = KayipStatus.objects.all()
    serializer_class = KayipStatusSerializer
