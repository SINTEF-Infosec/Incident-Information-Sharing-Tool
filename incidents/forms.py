from django import forms
import uuid
from datetimewidget.widgets import DateTimeWidget

from incidents.models import *

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('format', 'file')
        
        widgets = {
                   'format': forms.Select(attrs={'autofocus':'true'}),
                   }

class CustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        fields = ('incident_type', 'name', 'description', 'type')
        
        widgets = {
                   'incident_type': forms.HiddenInput(),
                   'name': forms.TextInput(attrs={'autofocus':'true'}),
                   }

class IncidentForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        entity = kwargs.pop('entity')
        super(IncidentForm, self).__init__(*args, **kwargs)
        
        liasions = Liaison.objects.filter(provider = entity) 
        
        choices = []
        for liasion in liasions:
            choices.append((liasion.id, liasion.name))
        
        self.fields['liaison'].choices = choices
        
        types = IncidentType.objects.filter(provider = entity)
        
        choices = []
        for type in types:
            choices.append((type.id, type.name))
        
        self.fields['type'].choices = choices
    
    class Meta:
        model = Incident
        fields = ('parent', 'type', 'language', 'status', 'impact', 'summary', 'description', 'occurrence_time', 'detection_time', 'liaison', 'next_update')
        
        widgets = {
                   'type': forms.Select(attrs={'autofocus':'true'}),
                   'occurrence_time': DateTimeWidget(attrs={}, usel10n = True, bootstrap_version=3),
                   'detection_time': DateTimeWidget(attrs={}, usel10n = True, bootstrap_version=3),
                   'parent': forms.HiddenInput(),
                   }

class SubscriberForm(forms.ModelForm):
    inputId = forms.CharField(max_length=36, required=False)
    token_end_point = forms.URLField(required = False)
    client_id = forms.CharField(max_length=255, required = False)
    client_secret = forms.CharField(max_length=255, required = False)
    
    class Meta:
        model = Entity
        fields = ('name', 'description', 'endpoint', 'provider')
        
        widgets = {
                   'name': forms.TextInput(attrs={'autofocus':'true'}),
                   }

class ProviderForm(forms.ModelForm):
    inputId = forms.CharField(max_length=36, required=False)
    token_end_point = forms.URLField(required = False)
    client_id = forms.CharField(max_length=255, required = False)
    client_secret = forms.CharField(max_length=255, required = False)
    
    class Meta:
        model = Entity
        fields = ('name', 'description', 'endpoint')
        
        widgets = {
                   'endpoint': forms.TextInput(attrs={'autofocus':'true'}),
                   }

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = ('name', 'description', 'endpoint', 'apple_url')
        
        widgets = {
                   'name': forms.TextInput(attrs={'autofocus':'true'}),
                   }

class IncidentTypeForm(forms.ModelForm):
    class Meta:
        model = IncidentType
        fields = ('name', 'description', 'consequence')
        
        widgets = {
                   'name': forms.TextInput(attrs={'autofocus':'true'}),
                   }

class TriggerTypeForm(forms.ModelForm):
    incident_type = forms.CharField(required = False, widget=forms.HiddenInput())
    
    def clean_incident_type(self):
        value = self.cleaned_data.get('incident_type')
        if value != "":
            incident = IncidentType()
            incident.id = uuid.UUID(value)
            
            return incident
        return value 
    
    class Meta:
        model = TriggerType
        fields = ('incident_type', 'name', 'description', 'comparators')
        
        widgets = {
                   'incident_type' : forms.HiddenInput(),
                   'name': forms.TextInput(attrs={'autofocus':'true'}),
                   }

class NotificationTypeForm(forms.ModelForm):
    class Meta:
        model = NotificationType
        fields = ('name', 'endpoint')
        
        widgets = {
                   'name': forms.TextInput(attrs={'autofocus':'true'}),
                   }

class NotificationIncidentForm(forms.ModelForm):
    notification_type = forms.CharField(required=False, widget=forms.HiddenInput())
    
    def clean_notification_type(self):
        value = self.cleaned_data.get('notification_type')
        if value != "":
            type = NotificationType()
            type.id = uuid.UUID(value)
            
            return type
        return value
    
    class Meta:
        model = NotificationIncident
        fields = ('name', 'type', 'notification_type')
        
        widgets = {
                   'name': forms.TextInput(attrs={'autofocus':'true'}),
                   }

class NotificationTriggerForm(forms.ModelForm):
    notification_incident = forms.CharField(required=False, widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        type = kwargs.pop('incidentType')
        super(NotificationTriggerForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = TriggerType.objects.filter(incident_type = type.id)
    
    def clean_notification_incident(self):
        value = self.cleaned_data.get('notification_incident')
        if value != "":
            incident = NotificationIncident()
            incident.id = uuid.UUID(value)
            
            return incident
        return value
    
    class Meta:
        model = NotificationTrigger
        fields = ('type', 'method', 'threshold', 'comparator', 'notification_incident')
        
        widgets = {
                   'type': forms.Select(attrs={'autofocus':'true'}),
                   }