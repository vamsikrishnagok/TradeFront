from django.urls import path
from django.conf.urls import url, handler404, handler500

from . import views
app_name = 'trademsg'

urlpatterns = [
    path('',views.index, name='index'),
    path('buy/',views.buy, name='buy'),
    path('sell/',views.sell, name='sell'),
    path('set_apikey/',views.set_apikey, name='setapikey'),
    path('set_accesstoken/',views.token, name='token'),
    path('reset/',views.reset, name='reset'),
    url(r'^login/$', views.auth_views.login, {'template_name': 'registration/login.html'},name='login'),
    url(r'^logout/$', views.auth_views.logout,{'template_name': 'registration/logout.html'},name='logout'),

    path('trademsg_lf/',views.trademsglf, name='trademsglf'),
    path('trademsglfsql/',views.trademsglfsql, name='trademsglfsql'),
    path('trademsghfsql/',views.trademsghfsql, name='trademsghfsql'),
    path('set_access_token/',views.set_access_token, name='set_access_token'),

    path('momo/',views.momo, name='momo'),
    path('momo_high/',views.momo_high, name='momo_high'),



    path('inter_report/',views.inter_report, name='inter_report'),
    path('inter_report_high/',views.inter_report_high, name='inter_report_high'),
    path('trade_high/',views.trade_high, name='trade_high'),

    path('pending_orders/',views.pending_orders, name='pending_orders'),

]