from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, View, DeleteView
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from datetime import datetime

from oauth2_provider.models import Application 

from incidents.models import *
from incidents.forms import *
from incidents.serializers import EntitySerializer

from sending.send import Sender
from rest_framework.renderers import JSONRenderer
import requests

from braces.views import LoginRequiredMixin

# TODO Remove in favour of plugins or signals
from a_ppl_e.models import EnduserNotification
import json
import ast

class Reset(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'dashboard'
    
    def get_redirect_url(self, *args, **kwargs):
        Entity.objects.all().delete()
        Incident.objects.all().delete()
        IncidentType.objects.all().delete()
        TriggerType.objects.all().delete()
        NotificationType.objects.all().delete()
        NotificationIncident.objects.all().delete()
        NotificationTrigger.objects.all().delete()
        Liaison.objects.all().delete()
        Notification.objects.all().delete()
        Attachment.objects.all().delete()
        CustomFieldValue.objects.all().delete()
        CustomField.objects.all().delete()
        AlertStatus.objects.all().delete()
        Alert.objects.all().delete()
        IncidentNotificationStatus.objects.all().delete()
        
        # Add providers
        provider = Entity()
        provider.id = uuid.UUID("7bd2ba88-71a7-470d-88ac-cb1bc288cf14")
        provider.name = "DataSpacer"
        provider.description = "DataSpacer is an IaaS"
        provider.endpoint = "http://dataspacer.herokuapp.com/api/1.0"
        provider.owner = True
        provider.provider = True
        provider.apple_url = ""
        provider.save()
        
        dtmt = Entity()
        dtmt.id = uuid.UUID("48681db4-2055-4887-a65a-51e513e25305")
        dtmt.name = "DTMT - DataSpacer"
        dtmt.description = "DTMT detects problems with geographic locations of data"
        dtmt.endpoint = ""
        dtmt.owner = False
        dtmt.provider = True
        dtmt.apple_url = ""
        dtmt.save()
        
        kardiomon = Entity()
        kardiomon.id = uuid.UUID("151fd89a-2ec5-463c-870d-45f9b2eacb21")
        kardiomon.name = "Kardio-Mon"
        kardiomon.description = "Kardio-Mon is a SaaS"
        kardiomon.endpoint = "http://kardio-mon.herokuapp.com/api/1.0"
        kardiomon.owner = False
        kardiomon.provider = False
        kardiomon.apple_url = ""
        kardiomon.save()
        
        # Add incident types
        outside = IncidentType()
        outside.id = uuid.UUID("4af8a5b7-309f-44c0-9dfe-3b54589aed0d")
        outside.name = "Data have been stored in unauthorized country"
        outside.description = "Data has been stored in an unauthorized country as defined in the data policy"
        outside.consequence = 0.9
        outside.provider = provider
        outside.save()
        
        resources = CustomField()
        resources.incident_type = outside
        resources.name = "resources"
        resources.description = "The affected resources, encoded in a JSON array"
        resources.type = "string"
        resources.save()
        
        users = CustomField()
        users.incident_type = outside
        users.name = "users"
        users.description = "The affected users, encoded in a JSON array"
        users.type = "string"
        users.save()
        
        spying = IncidentType()
        spying.id = uuid.UUID("293fdb5f-88d8-4290-ba02-ef09381e29e1")
        spying.name = "Unauthorized government access to data"
        spying.description = "Data (might) have been accessed by an unauthorized government"
        spying.consequence = 1.0
        spying.provider = provider
        spying.save()
        
        resources = CustomField()
        resources.incident_type = spying
        resources.name = "resources"
        resources.description = "The affected resources, encoded in a JSON array"
        resources.type = "string"
        resources.save()
        
        users = CustomField()
        users.incident_type = spying
        users.name = "users"
        users.description = "The affected users, encoded in a JSON array"
        users.type = "string"
        users.save()
        
        dataSpacerLiasion = Liaison()
        dataSpacerLiasion.name = "Andrew Smith"
        dataSpacerLiasion.email = "andrew.smith@data-spacer.com"
        dataSpacerLiasion.phone = "+44 (0115) 958 4567"
        dataSpacerLiasion.address = "Derby Rd."
        dataSpacerLiasion.zip = "NG1 5AD"
        dataSpacerLiasion.city = "Nottingham"
        dataSpacerLiasion.provider = provider
        dataSpacerLiasion.save()
        
        dataSpacerLiasion = Liaison()
        dataSpacerLiasion.name = "Teresa Jane"
        dataSpacerLiasion.email = "teresa.jane@kardio-mon.co.uk"
        dataSpacerLiasion.phone = "+44 (0117) 435 5589"
        dataSpacerLiasion.address = "16 Backfields Ln"
        dataSpacerLiasion.zip = "BS2 8QW"
        dataSpacerLiasion.city = "Bristol"
        dataSpacerLiasion.provider = kardiomon
        dataSpacerLiasion.save()
        
        subscription = NotificationType()
        subscription.name = "Data Transfer incidents"
        subscription.endpoint = "http://kardio-mon.herokuapp.com/api/1.0/receive"
        subscription.subscriber = kardiomon
        subscription.provider = provider
        subscription.save()
        
        subInc = NotificationIncident()
        subInc.name = "Data stored outside agreed area"
        subInc.type = outside
        subInc.notification_type = subscription
        subInc.provider = provider
        subInc.save()
        
        return super(Reset, self).get_redirect_url(*args, **kwargs)

# Main dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

class CompanyProfileEdit(LoginRequiredMixin, UpdateView):
    model = Entity
    form_class = CompanyProfileForm
    template_name = "company/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('company-profile')
    
    def get_context_data(self, **kwargs):
        context = super(CompanyProfileEdit, self).get_context_data(**kwargs)
        
        context['entity'] = Entity.objects.get(owner = True)
        
        return context
    
    def get_object(self, queryset=None):
        return Entity.objects.get(owner = True)
    

def _is_tlp_value(key):
    return key.startswith("tlp-")

def _get_field_name_from_tlp_field(tlp_field):
    prefix = "tlp-"
    return tlp_field[len(prefix):]

def slicedict(d, s):
    return {k:v for k,v in d.items() if k.startswith(s)}

def _handle_tlp(incident, form, request):
    post = request.POST
    
    schema = post.get('tlp_schema')
    main_value = post.get('tlp_value')
    
    tlp = incident.tlp
    if not tlp:
        tlp = TLP()
    
    tlp.schema = schema
    tlp.value = main_value
    tlp.save()
    tlp.remove_fields()
    
    incident.tlp = tlp
    incident.save()
    
    tlp_fields = slicedict(post, "tlp-")
    
    for k in tlp_fields:
        print(k)
        if _is_tlp_value(k):
            field = TLPField()
            field_name = _get_field_name_from_tlp_field(k)
            field.field = field_name
            field.value = post.get(k)
            tlp.add_field(field)

#
# This part handles actual incidents either received from other providers or
# created by internal human incident handlers
#
class IncidentList(LoginRequiredMixin, ListView):
    model = Incident
    template_name = "incidents/list.html"
    context_object_name = "items"
    paginate_by = 10

class IncidentCreate(LoginRequiredMixin, CreateView):
    form_class = IncidentForm
    model = Incident
    template_name = "incidents/edit.html"
    success_url = reverse_lazy('incident-list')
    
    def get_context_data(self, **kwargs):
        context = super(IncidentCreate, self).get_context_data(**kwargs)
        context['edit'] = False
        context['tlp_fields'] = []
        context['parent'] = self._get_parent()
        context['tlp_schema'] = ''
        context['tlp_value'] = ''
        return context
    
    def _get_parent(self):
        parent = self.request.GET.get('parent')
        if parent:
            return Incident.objects.get(pk = parent)
        return None
    
    def get_initial(self):
        initial = super(IncidentCreate, self).get_initial()
        
        parent = self._get_parent()
        
        if parent:
            initial['parent'] = parent.id
            initial['occurrence_time'] = parent.occurrence_time
            initial['detection_time'] = parent.detection_time
        
        return initial
    
    def get_form_kwargs(self):
        kwargs = super(IncidentCreate, self).get_form_kwargs()
        
        entity = Entity.objects.get(owner = True)
        
        kwargs['entity'] = entity
        
        return kwargs
    
    def form_valid(self, form):
        result = super(IncidentCreate, self).form_valid(form)
        
        custom_fields = CustomField.objects.filter(incident_type = self.object.type)
        
        for field in custom_fields:
            value = CustomFieldValue()
            value.type = field
            value.incident = self.object
            value.value = self.request.POST.get(str(field.id), "")
            
            value.save()
        
        _handle_tlp(self.object, form, self.request)
        
        status, created = IncidentNotificationStatus.objects.get_or_create(incident = self.object)
        status.notified = False
        status.save()
        
        return result

class IncidentDetails(LoginRequiredMixin, DetailView):
    model = Incident
    template_name = "incidents/details.html"
    
    def get_context_data(self, **kwargs):
        context = super(IncidentDetails, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['attachments'] = Attachment.objects.filter(incident__id = pk)
        
        custom_values = CustomFieldValue.objects.filter(incident__id = pk)
        context['custom_values'] = custom_values
        context['end_user_notifications'] = EnduserNotification.get_end_user_notification_for_incident(pk)
        
        resources = []
        users = []
        
        context['invalid_resources'] = False
        context['invalid_users'] = False
        
        # TODO fix hacky implementation
        for value in custom_values:
            if value.type.name == 'resources':
                if value.value:
                    try:
                        resources = json.loads(value.value, strict = False)
                    except ValueError:
                        try:
                            resources = ast.literal_eval(value.value)
                            value.value = json.dumps(resources)
                            value.save()
                            resources = json.loads(value.value)
                        except:
                            context['invalid_resources'] = True
            if value.type.name == 'users':
                if value.value:
                    try:
                        users = json.loads(value.value, strict = False)
                    except ValueError:
                        try:
                            users = ast.literal_eval(value.value)
                            value.value = json.dumps(users)
                            value.save()
                            users = json.loads(value.value)
                        except:
                            context['invalid_users'] = True
        
        context['notification_resources'] = resources
        context['notification_users'] = users
        
        context['tlp'] = self.object.tlp
        context['tlp_fields'] = TLPField.objects.filter(tlp = self.object.tlp)
        
        if self.object.tlp:
            context['tlp_schema'] = self.object.tlp.schema
            context['tlp_value'] = self.object.tlp.value
        else:
            context['tlp_schema'] = ''
            context['tlp_value'] = ''
        
        return context

class IncidentEdit(LoginRequiredMixin, UpdateView):
    model = Incident
    form_class = IncidentForm
    template_name = "incidents/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-details', kwargs={'pk': self.kwargs.get('pk')})
    
    def get_context_data(self, **kwargs):
        context = super(IncidentEdit, self).get_context_data(**kwargs)
        context['edit'] = True
        values = CustomFieldValue.objects.filter(incident__id = self.kwargs.get('pk'))
        dictionary = {}
        for value in values:
            dictionary[str(value.type.id)] = value.value
            
        context['custom_values'] = dictionary
        context['incidentId'] = self.object.id
        context['tlp'] = self.object.tlp
        context['tlp_fields'] = TLPField.objects.filter(tlp = self.object.tlp)
        
        if self.object.tlp:
            context['tlp_schema'] = self.object.tlp.schema
            context['tlp_value'] = self.object.tlp.value
        else:
            context['tlp_schema'] = ''
            context['tlp_value'] = ''
        
        return context
    
    def get_form_kwargs(self):
        kwargs = super(IncidentEdit, self).get_form_kwargs()
        
        entity = Entity.objects.get(owner = True)
        
        kwargs['entity'] = entity
        
        return kwargs
    
    def form_valid(self, form):
        result = super(IncidentEdit, self).form_valid(form)
        
        
        custom_fields = CustomField.objects.filter(incident_type = self.object.type)
        
        for field in custom_fields:
            try:
                value = CustomFieldValue.objects.get(type = field, incident = self.object)
            except:
                value = CustomFieldValue()
            
            newValue = CustomFieldValue()
            newValue.id = value.id
            newValue.type = field
            newValue.incident = self.object
            newValue.value = self.request.POST.get(str(field.id), "")
            
            newValue.save()
        
        _handle_tlp(self.object, form, self.request)
        
        status, created = IncidentNotificationStatus.objects.get_or_create(incident = self.object)
        status.notified = False
        status.save()

        return result

#
# Subscribers are the next link in the incident exchange chain. A subscriber could
# be a local authority, a customer, a log system, or another provider.
#
class SubscriberList(LoginRequiredMixin, ListView):
    model = Entity
    context_object_name = "items"
    paginate_by = 10
    template_name = "subscribers/list.html"
    
    def get_queryset(self):
        return self.model.objects.filter(provider = False)

def add_auth(entity, user, form):
    if "client_id" in form.cleaned_data:
        if "client_secret" in form.cleaned_data:
            if "token_end_point" in form.cleaned_data:
                id = form.cleaned_data['client_id']
                secret = form.cleaned_data['client_secret']
                end_point = form.cleaned_data['token_end_point']
                
                client = OAuthRemoteClient()
                client.client_id = id
                client.client_secret = secret
                client.token_endpoint = end_point
                client.entity = entity
                client.save()
    
    application = Application()
    application.user = user
    application.client_type = 'confidential'
    application.authorization_grant_type = 'client-credentials'
    application.name = entity.name
    application.save()
    
    entityOA = EntityOAuth()
    entityOA.entity = entity
    entityOA.application = application
    entityOA.save()

class SubscriberCreate(LoginRequiredMixin, CreateView):
    form_class = SubscriberForm
    model = Entity
    template_name = "subscribers/edit.html"
    success_url = reverse_lazy('subscriber-list')
    
    def form_valid(self, form):
        form.instance.provider = False
        
        if "inputId" in form.cleaned_data:
            provider_id = form.cleaned_data['inputId']
            
            if provider_id != "":
                form.instance.id = provider_id
        
        result = super(SubscriberCreate, self).form_valid(form)
        
        add_auth(self.object, self.request.user, form)
        # TODO add auth
        
        return result
    
    def get_context_data(self, **kwargs):
        context = super(SubscriberCreate, self).get_context_data(**kwargs)
        context['edit'] = False
        return context

class SubscriberEdit(LoginRequiredMixin, UpdateView):
    model = Entity
    form_class = SubscriberForm
    template_name = "subscribers/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-details', kwargs={'pk': self.kwargs.get('pk')})
    
    def get_context_data(self, **kwargs):
        context = super(SubscriberEdit, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

class SubscriberDetails(LoginRequiredMixin, DetailView):
    model = Entity
    template_name = "subscribers/details.html"
    
    def get_context_data(self, **kwargs):
        context = super(SubscriberDetails, self).get_context_data(**kwargs)
        
        subscriber = Entity()
        subscriber.id = self.kwargs.get('pk')
        
        context['subscriptions'] = NotificationType.objects.filter(subscriber = subscriber)
        
        return context

class SubscriberDelete(LoginRequiredMixin, DeleteView):
    model = Entity
    success_url = reverse_lazy('subscriber-list')
    template_name = "subscribers/delete.html"

#
# Providers are the previous link in the incident exchange chain. This is where the incident system
# receives incidents from. That be sensors, service providers, incident pools, etc.
#
class ProviderList(LoginRequiredMixin, ListView):
    model = Entity
    context_object_name = "items"
    paginate_by = 10
    template_name = "providers/list.html"
    
    def get_queryset(self):
        return self.model.objects.filter(provider = True, owner = False)

class ProviderCreate(LoginRequiredMixin, CreateView):
    form_class = ProviderForm
    model = Entity
    template_name = "providers/edit.html"
    success_url = reverse_lazy('provider-list')
    
    def form_valid(self, form):
        
        if "inputId" in form.cleaned_data:
            provider_id = form.cleaned_data['inputId']
            
            if provider_id != "":
                form.instance.id = provider_id
        
        result = super(ProviderCreate, self).form_valid(form)
        
        add_auth(self.object, self.request.user, form)
        
        # Add this instance as subscriber at provider
        self._add_current_instance_as_subscriber_at_provider()
        
        return result
    
    def get_context_data(self, **kwargs):
        context = super(ProviderCreate, self).get_context_data(**kwargs)
        context['edit'] = False
        return context
    
    def _add_current_instance_as_subscriber_at_provider(self):
        if self.object.endpoint:
            entity = Entity.objects.get(owner = True)
            provider = self.object
            
            encoded = EntitySerializer(entity, context={'request': self.request})
            payload = JSONRenderer().render(encoded.data)
            
            with open('payload.json', 'w') as jsonfile:
                jsonfile.write(str(payload))
            
            endpoint = provider.endpoint + '/subscriber'
            
            params = {'format': 'json'}
            r = requests.post(endpoint, data=payload, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, params=params, verify=False)

class ProviderDetails(LoginRequiredMixin, DetailView):
    model = Entity
    template_name = "providers/details.html"
    
    def get_context_data(self, **kwargs):
        context = super(ProviderDetails, self).get_context_data(**kwargs)
        
        return context

class ProviderEdit(LoginRequiredMixin, UpdateView):
    model = Entity
    form_class = ProviderForm
    template_name = "providers/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('provider-details', kwargs={'pk': self.kwargs.get('pk')})
    
    def get_context_data(self, **kwargs):
        context = super(ProviderEdit, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

class ProviderDelete(LoginRequiredMixin, DeleteView):
    model = Entity
    success_url = reverse_lazy('provider-list')
    template_name = "providers/delete.html"

#
# Incident types is a way of dynamically categorize incidents and control which 
# incidents each subscriber is allowed to receive.
#
class IncidentTypeList(LoginRequiredMixin, ListView):
    model = IncidentType
    context_object_name = "items"
    paginate_by = 10
    template_name = "incidents/types/list.html"
    
    def get_queryset(self):
        owner = Entity.objects.get(owner = True)
        return self.model.objects.filter(provider = owner)

class IncidentTypeCreate(LoginRequiredMixin, CreateView):
    model = IncidentType
    form_class = IncidentTypeForm
    template_name = "incidents/types/edit.html"
    success_url = reverse_lazy('incident-type-list')
    
    def get_context_data(self, **kwargs):
        context = super(IncidentTypeCreate, self).get_context_data(**kwargs)
        context['edit'] = False
        return context

class IncidentTypeDetails(LoginRequiredMixin, DetailView):
    model = IncidentType
    template_name = "incidents/types/details.html"
    
    def get_context_data(self, **kwargs):
        context = super(IncidentTypeDetails, self).get_context_data(**kwargs)
        
        context['triggers'] = TriggerType.objects.filter(incident_type = self.object)
        context['custom_fields'] = CustomField.objects.filter(incident_type = self.object)
        
        return context

class IncidentTypeEdit(LoginRequiredMixin, UpdateView):
    model = IncidentType
    form_class = IncidentTypeForm
    template_name = "incidents/types/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-type-details', kwargs={'pk': self.kwargs.get('pk')})
    
    def get_context_data(self, **kwargs):
        context = super(IncidentTypeEdit, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

class IncidentTypeDelete(LoginRequiredMixin, DeleteView):
    model = IncidentType
    template_name = "incidents/types/delete.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-type-details', kwargs={'pk': self.kwargs.get('pk')})

#
# Triggers Types are a way of defining which conditions the subscriber might select to demand
# a notification 
#
class TriggerTypeEdit(LoginRequiredMixin, UpdateView):
    model = TriggerType
    template_name = "triggers/types/edit.html"
    form_class = TriggerTypeForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-type-details', kwargs={'pk': self.kwargs.get('incidentType')})
    
    def get_context_data(self, **kwargs):
        context = super(TriggerTypeEdit, self).get_context_data(**kwargs)
        context['edit'] = True
        return context
    
    def form_valid(self, form):
        incident_type = IncidentType()
        incident_type.id = self.kwargs.get('incidentType')
        form.instance.incident_type = incident_type
        
        return super(TriggerTypeEdit, self).form_valid(form)

class TriggerTypeCreate(LoginRequiredMixin, CreateView):
    model = TriggerType
    template_name = "triggers/types/edit.html"
    form_class = TriggerTypeForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-type-details', kwargs={'pk': self.kwargs.get('incidentType')})
    
    def form_valid(self, form):
        incident_type = IncidentType()
        incident_type.id = self.kwargs.get('incidentType')
        form.instance.incident_type = incident_type
        
        return super(TriggerTypeCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(TriggerTypeCreate, self).get_context_data(**kwargs)
        context['edit'] = False
        return context

class TriggerTypeDelete(LoginRequiredMixin, DeleteView):
    model = TriggerType
    template_name = "triggers/types/delete.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-type-details', kwargs={'pk': self.kwargs.get('incidentType')})

class CustomFieldCreate(LoginRequiredMixin, CreateView):
    model = CustomField
    form_class = CustomFieldForm
    template_name = "incidents/customField/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-type-details', kwargs={'pk': self.kwargs.get('incidentType')})
    
    def get_initial(self):
        initial = super(CustomFieldCreate, self).get_initial()
        
        initial['incident_type'] = self.kwargs.get('incidentType')
        
        return initial

class CustomFieldEdit(LoginRequiredMixin, UpdateView):
    model = CustomField
    form_class = CustomFieldForm
    template_name = "incidents/customField/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-type-details', kwargs={'pk': self.kwargs.get('incidentType')})
    
    def get_context_data(self, **kwargs):
        context = super(CustomFieldEdit, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

class CustomFieldDelete(LoginRequiredMixin, DeleteView):
    model = CustomField
    template_name = "incidents/customField/delete.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-type-details', kwargs={'pk': self.kwargs.get('incidentType')})
#
# A provider subscription is an agreement between A and B, where A receives incident
# notifications from B. 
#
# The notification subscriptions are added by utilizing the API of B. 
#
## TODO: REWRITE TO USE EXTERNAL API
class ProviderSubscriptionCreate(LoginRequiredMixin, CreateView):
    model = NotificationType
    form_class = NotificationTypeForm
    template_name = "notifications/types/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('provider-details', kwargs={'pk': self.kwargs.get('provider')})
    
    def get_context_data(self, **kwargs):
        context = super(ProviderSubscriptionCreate, self).get_context_data(**kwargs)
        context['edit'] = False
        return context

#
# Subscriber Subscriptions are the opposite of Provider Subscriptions. Here B are able to add A
# This is handy in the case of e.g. local authorities - you would be able to add them yourself
# not having to wait for or ask them to add your system. 
#
class SubscriberSubscriptionCreate(LoginRequiredMixin, CreateView):
    model = NotificationType
    form_class = NotificationTypeForm
    template_name = "notifications/types/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-details', kwargs={'pk': self.kwargs.get('subscriber')})
    
    def form_valid(self, form):
        sub = Entity()
        sub.id = self.kwargs.get('subscriber')
        form.instance.subscriber = sub
        
        return super(SubscriberSubscriptionCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SubscriberSubscriptionCreate, self).get_context_data(**kwargs)
        context['edit'] = False
        return context

class SubscriberSubscriptionEdit(LoginRequiredMixin, UpdateView):
    model = NotificationType
    form_class = NotificationTypeForm
    template_name = "notifications/types/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-details', kwargs={'pk': self.kwargs.get('subscriber')})
    
    def form_valid(self, form):
        sub = Entity()
        sub.id = self.kwargs.get('subscriber')
        form.instance.subscriber = sub
        
        return super(SubscriberSubscriptionEdit, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SubscriberSubscriptionEdit, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

class SubscriberSubscriptionDetails(LoginRequiredMixin, DetailView):
    model = NotificationType
    template_name = "notifications/types/details.html"
    
    def get_context_data(self, **kwargs):
        context = super(SubscriberSubscriptionDetails, self).get_context_data(**kwargs)
        context['incidents'] = NotificationIncident.objects.filter(notification_type = self.object)
        return context

class SubscriberSubscriptionDelete(LoginRequiredMixin, DeleteView):
    model = NotificationType
    template_name = "notifications/types/delete.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-subscription-details', kwargs={'pk': self.kwargs.get('pk'), 'subscriber': self.kwargs.get('subscriber')})
    
    
class SubscriberSubscriptionIncidentCreate(LoginRequiredMixin, CreateView):
    model = NotificationIncident
    form_class = NotificationIncidentForm
    template_name = "notifications/incidents/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-subscription-details', kwargs={'subscriber': self.kwargs.get('subscriber'), 'pk': self.kwargs.get('subscription')})
    
    def form_valid(self, form):
        type = NotificationType()
        type.id = self.kwargs.get('subscription')
        form.instance.notification_type = type
        
        return super(SubscriberSubscriptionIncidentCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SubscriberSubscriptionIncidentCreate, self).get_context_data(**kwargs)
        context['edit'] = False
        return context

class SubscriberSubscriptionIncidentEdit(LoginRequiredMixin, UpdateView):
    model = NotificationIncident
    form_class = NotificationIncidentForm
    template_name = "notifications/incidents/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-subscription-details', kwargs={'subscriber': self.kwargs.get('subscriber'), 'pk': self.kwargs.get('subscription')})
    
    def form_valid(self, form):
        type = NotificationType()
        type.id = self.kwargs.get('subscription')
        form.instance.notification_type = type
        
        return super(SubscriberSubscriptionIncidentEdit, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SubscriberSubscriptionIncidentEdit, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

class SubscriberSubscriptionIncidentDelete(LoginRequiredMixin, DeleteView):
    model = NotificationIncident
    template_name = "notifications/incidents/delete.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-subscription-details', kwargs={'subscriber': self.kwargs.get('subscriber'), 'pk': self.kwargs.get('subscription')})

class SubscriptionTriggerCreate(LoginRequiredMixin, CreateView):
    model = NotificationTrigger
    form_class = NotificationTriggerForm
    template_name = "notifications/triggers/edit.html"
    
    def get_form_kwargs(self):
        kwargs = super(SubscriptionTriggerCreate, self).get_form_kwargs()
        incidentId = self.kwargs.get('incident')
        id = uuid.UUID(incidentId)
        incident = NotificationIncident.objects.get(pk = id)
        kwargs['incidentType'] = incident.type
        
        return kwargs
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-subscription-details', kwargs={'subscriber': self.kwargs.get('subscriber'), 'pk': self.kwargs.get('subscription')})
    
    def form_valid(self, form):
        incident = NotificationIncident()
        incident.id = self.kwargs.get('incident')
        form.instance.notification_incident = incident
        
        return super(SubscriptionTriggerCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SubscriptionTriggerCreate, self).get_context_data(**kwargs)
        context['edit'] = False
        return context

class SubscriptionTriggerEdit(LoginRequiredMixin, UpdateView):
    model = NotificationTrigger
    form_class = NotificationTriggerForm
    template_name = "notifications/triggers/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-subscription-details', kwargs={'subscriber': self.kwargs.get('subscriber'), 'pk': self.kwargs.get('subscription')})
    
    def get_form_kwargs(self):
        kwargs = super(SubscriptionTriggerEdit, self).get_form_kwargs()
        incidentId = self.kwargs.get('incident')
        id = uuid.UUID(incidentId)
        incident = NotificationIncident.objects.get(pk = id)
        kwargs['incidentType'] = incident.type
        
        return kwargs
    
    def form_valid(self, form):
        incident = NotificationIncident()
        incident.id = self.kwargs.get('incident')
        form.instance.notification_incident = incident
        
        return super(SubscriptionTriggerEdit, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SubscriptionTriggerEdit, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

class SubscriptionTriggerDelete(LoginRequiredMixin, DeleteView):
    model = NotificationTrigger
    template_name = "notifications/triggers/delete.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('subscriber-subscription-details', kwargs={'subscriber': self.kwargs.get('subscriber'), 'pk': self.kwargs.get('subscription')})


class AttachmentCreate(LoginRequiredMixin, CreateView):
    model = Attachment
    form_class = AttachmentForm
    template_name = "incidents/attachments/edit.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-details', kwargs={'pk': self.kwargs.get('incident')})
    
    def form_valid(self, form):
        incident = Incident()
        incident.id = self.kwargs.get('incident')
        form.instance.incident = incident
        
        return super(AttachmentCreate, self).form_valid(form)

#
# View for handling sending notifications to subscribers
#
class Notify(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        incident_id = kwargs.get('incident')
        incident = Incident.objects.get(pk = incident_id)
         
        sender = Sender(request)
        sender.notify(incident)
        
        return redirect('incident-details', pk=kwargs.get('incident'), permanent=False)