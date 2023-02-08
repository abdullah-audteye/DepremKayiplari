from django.urls import include, path
from django.contrib import admin
from appname.views import IhbarView,KayipUserListView,KayipStatusListView


urlpatterns = [
    path("admin", admin.site.urls, name="admin_page"),
    path('',IhbarView,name="ihbarview_tr"),
    path('api/kayiplar',KayipUserListView.as_view(),name="kayiplarview_api"),
    path('api/kayipstatus',KayipStatusListView.as_view(),name="kayip_status_api")

]