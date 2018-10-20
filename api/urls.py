from django.conf.urls import include, url
from . import api as api_views

urlpatterns = [
    url(r'^user/login/$', api_views.UserLogin.as_view(), name='user-login'), 
    url(r'^user/balance/$', api_views.getBalance.as_view(), name='user-balance'), 
    url(r'^user/create/$', api_views.UserCreate.as_view(), name='user-create'), 
]