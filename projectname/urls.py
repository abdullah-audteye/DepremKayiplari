from django.urls import include, path
from django.contrib import admin
from appname.views import IhbarView,KayipUserList,KayipUserListAR,KayipUserListView,IhbarViewAR


urlpatterns = [
    path("admin", admin.site.urls, name="admin_page"),
    path('tr',IhbarView,name="ihbarview_tr"),
    path('ar',IhbarViewAR,name="ihbarview_ar"),

    path('tr/kayiplar',KayipUserList,name="kayiplarview_tr"),
    path('ar/kayiplar',KayipUserListAR,name="kayiplarview_ar"),

    path('api/kayiplar',KayipUserListView.as_view(),name="kayiplarview_api")

]