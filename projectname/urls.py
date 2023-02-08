from django.urls import include, path
from django.contrib import admin
from appname.views import IhbarView,KayipUserListView


urlpatterns = [
    path("admin", admin.site.urls, name="admin_page"),
    path('',IhbarView,name="ihbarview_tr"),
    path('api/kayiplar',KayipUserListView.as_view(),name="kayiplarview_api")

]