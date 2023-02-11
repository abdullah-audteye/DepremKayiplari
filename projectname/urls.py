from django.urls import include, path
from django.contrib import admin
from appname.views import IhbarView, KayipUserListView, KayipUserFilterUser, KayipStatusListView, ChangeKayipStatus, GeneralFormDataView, item_list, ReportListView, UpdateReportView
from users.views import login_view


urlpatterns = [
    path("admin", admin.site.urls, name="admin_page"),
    path('', IhbarView, name="ihbarview_tr"),
    path('kayiplar/durum/<int:pk>', ChangeKayipStatus,
         name="kayiplar_durum_detail"),
    path('genelform', GeneralFormDataView, name="genelform"),


    path('api/kayiplar', KayipUserListView.as_view(), name="kayiplarview_api"),

    path('api/kayiplar/filter', KayipUserFilterUser.as_view(),
         name="kayiplarview_api_filter"),
    path('api/kayipstatus', KayipStatusListView.as_view(), name="kayip_status_api"),


    path('table', item_list, name='item_list'),

    # Authentication paths
    path('login', login_view, name='login'),

    # Reports endpoints
    path('api/reports', ReportListView.as_view(), name="reportlist_api"),
    path('api/reports/<int:pk>', UpdateReportView.as_view(), name="reportlist_api_update"),
]

# urlpatterns = [    path('', item_list, name='item_list'),    path('edit/<int:pk>/', edit_item, name='edit_item'),]
