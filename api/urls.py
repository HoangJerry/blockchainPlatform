from django.conf.urls import include, url
from . import api as api_views

urlpatterns = [
    url(r'^user/login/$', api_views.UserLogin.as_view(), name='user-login'), 
    url(r'^user/me/$', api_views.UserInfor.as_view(), name='user-login'), 
    url(r'^user/balance/$', api_views.getBalance.as_view(), name='user-balance'), 
    url(r'^user/create/$', api_views.UserCreate.as_view(), name='user-create'), 
    url(r'^user/history/test/$', api_views.UserTestHistory.as_view(), name='user-create'), 
    url(r'^doctor/history/test/$', api_views.DoctorTestHistory.as_view(), name='user-create'), 
    url(r'^user/history/test/create/$', api_views.CreateTestHistory.as_view(), name='user-create'), 
    url(r'^user/history/test/update/(?P<pk>[0-9]+)/$', api_views.UpdateTestHistory.as_view(), name='user-create'), 
    
    url(r'^data/name-of-test/$', api_views.DataNameOfTest.as_view(), name='data-name-of-test'), 

]