from django.shortcuts import render, redirect
from .forms import KayipUserForm, IhbarUserForm
from .models import Ihbar, KayipUser, Tag, Countries, KayipStatus,IhbarUser,Cities
from django.db import transaction,IntegrityError
from django.http import JsonResponse
from django.http import QueryDict
from .serializers import  IhbarSerializer, KayipStatusSerializer,KayipUserSerializer, ReportSerializer,CitiesSerializer,KayipUserSerializerCertainParameters
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView,GenericAPIView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .helper import CleanBadRecords,FixNonHavingDates,SendAccessCode
from datetime import datetime
import random
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.cache import cache




def get_cities_from_file(path):
    try:
        with open(path, 'r') as f:
            cities = json.load(f)
        return cities

    except:
        return []




def CountriesAsJson(request):
    cities = list(Countries.objects.all().values())
    return JsonResponse(cities,safe=False)

class CitiesWithFilter(ListAPIView):
    serializer_class = CitiesSerializer

    def get_queryset(self,*args, **kwargs):
        country_id = (self.request.GET.get('countryId',None))
        cities = (Cities.objects.filter(country_id=country_id))
        return cities
        


@csrf_exempt
def ChangeKayipStatus(request,pk):
    ihbar = get_object_or_404(Ihbar,access_code=pk)
    kayip_status = KayipStatus.objects.all()

    if request.method == "POST":
        kayip_user_update = (request.POST.getlist('data[]'))
        try:
            for updated in kayip_user_update:
                kayipuserobj = (QueryDict(updated))
                if(kayipuserobj.get("status") == None) or kayipuserobj.get("user_id") == None :
                    continue
                kayip_user_instance = KayipUser.objects.get(id=kayipuserobj['user_id'])
                kayip_user_instance.kayip_status_id = kayipuserobj['status']
                kayip_user_instance.save()
            return JsonResponse({'status': True, 'message': "success"}, status=200)
        except Exception as err:
            # print(err,'errr')
            return JsonResponse({'status': False, 'message': "Failed"}, status=200)

    return render(request,'change_status.html',{"ihbar":ihbar,'kayip_status':kayip_status,"access_code":pk})


@csrf_exempt
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
            city = ihbarci_data.get('city')
            record_status = True

            try:
                with transaction.atomic():
                    ihbaruserform_instance = ihbaruserform.save()

                    saved_records = []
                    for kayip_user in kayip_user_data:
                        kayip_user = QueryDict(kayip_user).copy()
                        kayip_user['cordinate_x'] = cordinate_x
                        kayip_user['cordinate_y'] = cordinate_y
                        kayip_user['city'] = city


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

                        if(ihbaruserform_instance.eposta):
                            
                            toemail =ihbaruserform_instance.eposta
                            dynamic_template_data = {
                            "subject":"Your access code to change missing people's status",
                            "name":ihbar_instance.access_code,
                            "url":request.build_absolute_uri("/kayiplar/durum/"+str(ihbar_instance.access_code))
                            }

                            SendAccessCode(toemail,dynamic_template_data)
                        return JsonResponse({'status': True, 'message': "success"}, status=200)

                    else:
                        return JsonResponse({'status': False, 'message': "Failed"}, status=200)



            except IntegrityError:
                print("IntegrityError", 'errrr')

    return render(request, "ihbar.html",
                  {"kayipuserform": kayipuserform, "ihbaruserform": ihbaruserform, "tags": tags, "countries": countries,
                   "kayip_status": kayipstatus})



def GeneralFormDataView(request):
    countries = Countries.objects.all()
    cities = Cities.objects.all()
    kayipstatus = KayipStatus.objects.all()
    errors = {}

    if request.method == "POST":
        ihbaruserform = IhbarUserForm(request.POST)
        kayip_user_form = KayipUserForm(request.POST)

        if(ihbaruserform.is_valid() and kayip_user_form.is_valid()):
            with transaction.atomic():
                ihbaruser = ihbaruserform.save()
                kayip_user = kayip_user_form.save()


                ihbar_instance = Ihbar.objects.create()
                access_number = random.randint(000000,999999)

                ihbar_instance.ihbar_user = ihbaruser
                ihbar_instance.access_code = access_number
                ihbar_instance.kayip_user.add(kayip_user.id)
                ihbar_instance.created_time = datetime.now()
                ihbar_instance.save()
                if(ihbaruser.eposta):
                                
                    toemail =ihbaruser.eposta
                    dynamic_template_data = {
                    "subject":"Your access code to change missing people's status",
                    "name":ihbar_instance.access_code,
                    "url":request.build_absolute_uri("/kayiplar/durum/"+str(ihbar_instance.access_code))
                    }

                    SendAccessCode(toemail,dynamic_template_data)
                return redirect('ihbarview_tr')


        else:
            errors["errors"] = str(ihbaruserform.errors) or str(kayip_user_form.errors)
            
    return render(request,'generalformdata.html',{"countries":countries,"kayipstatus":kayipstatus,"errors":errors,"cities":cities})




class KayipUserWithCertainParametersListView(ListAPIView):
    queryset = KayipUser.objects.all().select_related()
    serializer_class = KayipUserSerializerCertainParameters

    def list(self, request, *args, **kwargs):
        if cache.get('kayip_user_with_params_qs') != None:
            cached_queryset = cache.get('kayip_user_with_params_qs')
            return Response(cached_queryset)

        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)

            cached_queryset = cache.set('kayip_user_with_params_qs',serializer.data,60*3)
            return Response(serializer.data)


class IhbarDetailRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Ihbar.objects.all()
    serializer_class = IhbarSerializer
    lookup_url_kwarg = "kayip_user_id"
    lookup_field = "kayip_user"



class KayipUserListView(ListAPIView):
    queryset = Ihbar.objects.order_by('-id').prefetch_related('kayip_user').select_related('ihbar_user')
    serializer_class = IhbarSerializer


class CreateIhbarciandKayip(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        ihbar_user_obj = {
            "ihbar_first_name":data.get('ihbar_first_name',"None"),
            "ihbar_last_name":data.get('ihbar_last_name',"None"),
            "phonenumber":data.get('phonenumber',"None"),
            "eposta":data.get('phonenumber',"none@none.com")
        }

        kayip_user_obj = {
            "kayip_first_name":data.get('kayip_first_name',"None"),
            "kayip_last_name":data.get('kayip_last_name',"None"),
            # "cordinate_x":data.get('cordinate_x',0),
            # "cordinate_y":data.get('cordinate_y',0),
            "address":data.get('address',None),
            "detail":data.get('detail',None),
            "status":data.get('status',None),
            "kayip_status_id":data.get('kayip_status',None),
            "gender":data.get('gender',"M"),
        }

        with transaction.atomic():

            try:

                ihbar_user_instance = IhbarUser.objects.create(**ihbar_user_obj)
                kayip_user_instance = KayipUser.objects.create(**kayip_user_obj)
                ihbar_instance = Ihbar.objects.create()
                access_number = random.randint(000000,999999)

                ihbar_instance.ihbar_user = ihbar_user_instance
                ihbar_instance.access_code = access_number
                ihbar_instance.kayip_user.add(kayip_user_instance.id)
                ihbar_instance.created_time = datetime.now()
                ihbar_instance.save()
            except IntegrityError as err:
                return Response(str(err),400)


        return Response('Success')


class KayipUserFilterUser(ListAPIView):
    serializer_class = KayipUserSerializer

    def get_queryset(self,*args, **kwargs):
        first_name_qs = (self.request.GET.get('first_name',None))
        queryset = KayipUser.objects.filter(kayip_first_name__icontains=first_name_qs)
        return queryset


    def get(self, request, *args, **kwargs):
        first_name_qs = (self.request.GET.get('first_name',None))
        if (first_name_qs) !=None and len(first_name_qs)<3:
            return Response({"error":"Must be at least 3 characters "},status=status.HTTP_400_BAD_REQUEST)
        return self.list(request, *args, **kwargs)

        



class KayipStatusListView(ListAPIView):
    queryset = KayipStatus.objects.all()
    serializer_class = KayipStatusSerializer


class ReportListView(ListAPIView):
    queryset = Ihbar.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication,]


class UpdateReportView(RetrieveUpdateDestroyAPIView):
    queryset = Ihbar.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication,]


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        kayip_user_id = request.data.get('reported_id')
        kayip_user_instance = KayipUser.objects.get(id=kayip_user_id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        serializer_kayip_user = KayipUserSerializer(kayip_user_instance, data=request.data, partial=partial)
        serializer_kayip_user.is_valid(raise_exception=True)
        serializer_kayip_user.save()
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

def item_list(request):
    if request.user.is_authenticated:
        items = KayipUser.objects.all()
        return render(request, 'item_list.html', {'items': items})
    else:
        return redirect('ihbarview_tr')