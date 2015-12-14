from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from incidents import api

urlpatterns = [
    #url(r'^1.0$', views.api_root, name='api_root'),
    
    url(r'^1.0/identity$', api.ProviderIdentity.as_view(), name='provider-identity'),
    url(r'^1.0/subscriber$', api.Subscriber.as_view(), name='subscriber'),
    
    url(r'^1.0/incidents/types$', api.IncidentTypeList.as_view(), name='incident-type-list'),
    url(r'^1.0/incidents/types/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', api.IncidentTypeDetail.as_view(), name='incidenttype-detail'),
    
    url(r'^1.0/incidents/types/(?P<incident>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/triggers/types$', api.TriggerTypeList.as_view(), name='triggertype-list'),
    url(r'^1.0/triggers/types/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', api.TriggerTypeDetail.as_view(), name='triggertype-detail'),
    
    url(r'^1.0/subscriptions$', api.NotificationTypeList.as_view(), name='notification-list'),
    url(r'^1.0/subscriptions/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', api.NotificationTypeDetail.as_view(), name='notificationtype-detail'),
    
    url(r'^1.0/subscriptions/(?P<notification>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/incidents$', api.NotificationIncidentList.as_view(), name='notification-incident-list'),
    url(r'^1.0/incidents/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', api.NotificationIncidentDetail.as_view(), name='notification-incident-detail'),
    
    url(r'^1.0/incidents/(?P<notificationIncident>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/triggers$', api.NotificationTriggerList.as_view(), name='notification-trigger-list'),
    url(r'^1.0/triggers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', api.NotificationTriggerDetail.as_view(), name='notification-trigger-detail'),
    
    url(r'^1.0/receive$', api.ReceiveNotification.as_view(), name='receive'),
    
    # custom field
    url(r'^1.0/incidents/types/(?P<incidentType>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/custom-fields$', api.CustomFieldList.as_view(), name='custom-field-list'),
    url(r'^1.0/incidents/(?P<incident>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/custom-fields/(?P<customFieldType>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', api.CustomFieldValueDetails.as_view(), name='custom-field-value-details'),
    
    url(r'^1.0/alerts', api.AlertStatusList.as_view(), name='alert-list'),
    url(r'^1.0/alerts/(?P<id>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))', api.AlertStatusRead.as_view(), name='alert-mark-read'),
    
    url(r'1.0/test-urls/incidents/(?P<incidentId>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/notify-end-users', api.SendEndUserNotification.as_view(), name='test-send-end-user-notification'),
    url(r'1.0/test-urls/incidents/(?P<incidentId>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/notify', api.SendNotification.as_view(), name='test-send-notification'),
    url(r'1.0/test-urls/incidents', api.IncidentList.as_view(), name='test-incident-list'),
    url(r'1.0/test-urls/incidents/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))', api.IncidentDetails.as_view(), name='test-incident-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)