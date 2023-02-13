from django.urls import include, path
from django.contrib import admin
from appname.views import IhbarView, KayipUserListView,CountriesAsJson,IhbarDetailRetrieveView,KayipUserWithCertainParametersListView, CitiesWithFilter,KayipUserFilterUser, KayipStatusListView, ChangeKayipStatus, GeneralFormDataView, item_list, ReportListView, UpdateReportView
from users.views import login_view


urlpatterns = [
    path("admin", admin.site.urls, name="admin_page"),
    path('', IhbarView, name="ihbarview_tr"),
    path('kayiplar/durum/<int:pk>', ChangeKayipStatus,name="kayiplar_durum_detail"),
    path('genelform', GeneralFormDataView, name="genelform"),

    path('api/kayiplar', KayipUserListView.as_view(), name="kayiplarview_api"),
    path('api/kayiplar/all', KayipUserWithCertainParametersListView.as_view(), name="kayiplarview_with_params_api"),
    path('api/kayiplar/<int:kayip_user_id>', IhbarDetailRetrieveView.as_view(), name="ihbar_detail_retrieve"),


    path('api/kayiplar/filter', KayipUserFilterUser.as_view(),name="kayiplarview_api_filter"),
    path('api/kayipstatus', KayipStatusListView.as_view(), name="kayip_status_api"),

    path('table', item_list, name='item_list'),

    # Authentication paths
    path('login', login_view, name='login'),

    path('api/cities',CitiesWithFilter.as_view(),name="cities_json"),
    path('api/countries',CountriesAsJson,name="countries_json"),


    # Reports endpoints
    path('api/reports', ReportListView.as_view(), name="reportlist_api"),
    path('api/reports/<int:pk>', UpdateReportView.as_view(), name="reportlist_api_update"),
]

