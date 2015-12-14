from django.conf.urls import patterns, url
from a_ppl_e import views

urlpatterns = patterns('',
    
    url(r'incidents/(?P<incident>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/notify-end-users/create$', views.NotifyEndUserView.as_view(), name='incident-notify-endusers'),
    
)