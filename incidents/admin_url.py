from django.conf.urls import patterns, url
from incidents import views

urlpatterns = patterns('',
    #url(r'^1.0$', views.api_root, name='api_root'),
    
    url(r'reset$', views.Reset.as_view(), name='reset'),
    
    url(r'dashboard$', views.DashboardView.as_view(), name='dashboard'),
    
    url(r'profile$', views.CompanyProfileEdit.as_view(), name='company-profile'),
    
    # Incidents
    url(r'incidents$', views.IncidentList.as_view(), name='incident-list'),
    url(r'incidents/new$', views.IncidentCreate.as_view(), name='incident-create'),
    url(r'incidents/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', views.IncidentDetails.as_view(), name='incident-details'),
    url(r'incidents/(?P<incident>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/notify-subscribers$', views.Notify.as_view(), name='incident-notify-subscribers'),
    url(r'incidents/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/edit$', views.IncidentEdit.as_view(), name='incident-edit'),
    
    # Attachment
    url(r'incidents/(?P<incident>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/attachments/new$', views.AttachmentCreate.as_view(), name='incident-attachment-create'),
    
    # Incident Types
    url(r'incidents/types$', views.IncidentTypeList.as_view(), name='incident-type-list'),
    url(r'incidents/types/new$', views.IncidentTypeCreate.as_view(), name='incident-type-create'),
    url(r'incidents/types/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', views.IncidentTypeDetails.as_view(), name='incident-type-details'),
    url(r'incidents/types/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/edit$', views.IncidentTypeEdit.as_view(), name='incident-type-edit'),
    url(r'incidents/types/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/delete$', views.IncidentTypeDelete.as_view(), name='incident-type-delete'),
    
    # Trigger Types
    url(r'incidents/types/(?P<incidentType>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/triggers/new$', views.TriggerTypeCreate.as_view(), name='trigger-type-create'),
    url(r'incidents/types/(?P<incidentType>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/triggers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/edit$', views.TriggerTypeEdit.as_view(), name='trigger-type-edit'),
    url(r'incidents/types/(?P<incidentType>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/triggers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/delete$', views.TriggerTypeDelete.as_view(), name='trigger-type-delete'),
    
    # Custom Fields
    url(r'incidents/types/(?P<incidentType>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/customfields/new$', views.CustomFieldCreate.as_view(), name='custom-field-create'),
    url(r'incidents/types/(?P<incidentType>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/customfields/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/edit$', views.CustomFieldEdit.as_view(), name='custom-field-edit'),
    url(r'incidents/types/(?P<incidentType>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/customfields/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/delete$', views.CustomFieldDelete.as_view(), name='custom-field-delete'),
    
    # Subscribers
    url(r'subscribers$', views.SubscriberList.as_view(), name='subscriber-list'),
    url(r'subscribers/new$', views.SubscriberCreate.as_view(), name='subscriber-create'),
    url(r'subscribers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', views.SubscriberDetails.as_view(), name='subscriber-details'),
    url(r'subscribers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/edit$', views.SubscriberEdit.as_view(), name='subscriber-edit'),
    url(r'subscribers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/delete', views.SubscriberDelete.as_view(), name='subscriber-delete'),
    
    # Notification Type Subscriber
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/new$', views.SubscriberSubscriptionCreate.as_view(), name='subscriber-subscription-create'),
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', views.SubscriberSubscriptionDetails.as_view(), name='subscriber-subscription-details'),
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/edit$', views.SubscriberSubscriptionEdit.as_view(), name='subscriber-subscription-edit'),
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/delete$', views.SubscriberSubscriptionDelete.as_view(), name='subscriber-subscription-delete'),
    
    # Notification Incidents
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/(?P<subscription>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/incident-types/new$', views.SubscriberSubscriptionIncidentCreate.as_view(), name='subscriber-subscription-incident-create'),
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/(?P<subscription>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/incident-types/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/edit$', views.SubscriberSubscriptionIncidentEdit.as_view(), name='subscriber-subscription-incident-edit'),
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/(?P<subscription>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/incident-types/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/delete$', views.SubscriberSubscriptionIncidentDelete.as_view(), name='subscriber-subscription-incident-delete'),
    
    # Notification Triggers
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/(?P<subscription>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/incidents/(?P<incident>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/triggers/new$', views.SubscriptionTriggerCreate.as_view(), name='subscriber-subscription-trigger-create'),
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/(?P<subscription>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/incidents/(?P<incident>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/triggers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', views.SubscriptionTriggerEdit.as_view(), name='subscriber-subscription-trigger-edit'),
    url(r'subscribers/(?P<subscriber>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/(?P<subscription>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/incidents/(?P<incident>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/triggers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/delete$', views.SubscriptionTriggerDelete.as_view(), name='subscriber-subscription-trigger-delete'),
    
    
    # Providers
    url(r'providers$', views.ProviderList.as_view(), name='provider-list'),
    url(r'providers/new$', views.ProviderCreate.as_view(), name='provider-create'),
    url(r'providers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))$', views.ProviderDetails.as_view(), name='provider-details'),
    url(r'providers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/edit$', views.ProviderEdit.as_view(), name='provider-edit'),
    url(r'providers/(?P<pk>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/delete$', views.ProviderDelete.as_view(), name='provider-delete'),
    
    # Notification Type Provider
    url(r'providers/(?P<provider>([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?))/subscriptions/new$', views.ProviderSubscriptionCreate.as_view(), name='provider-subscription-create'),
    
    
)