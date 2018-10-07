from django.conf.urls import include, url
from . import api as api_views

urlpatterns = [
    url(r'^user/$', api_views.UserList.as_view(), name='user-list'), 
]