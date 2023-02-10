from django.urls import include, path
from django.contrib import admin
from appname.views import IhbarView,KayipUserListView,KayipUserFilterUser,KayipStatusListView,ChangeKayipStatus,GeneralFormDataView


urlpatterns = [
    path("admin", admin.site.urls, name="admin_page"),
    path('',IhbarView,name="ihbarview_tr"),
    path('kayiplar/durum/<int:pk>',ChangeKayipStatus,name="kayiplar_durum_detail"),
    path('genelform',GeneralFormDataView,name="genelform"),


    path('api/kayiplar',KayipUserListView.as_view(),name="kayiplarview_api"),
    path('api/kayiplar/filter',KayipUserFilterUser.as_view(),name="kayiplarview_api_filter"),
    path('api/kayipstatus',KayipStatusListView.as_view(),name="kayip_status_api")

]