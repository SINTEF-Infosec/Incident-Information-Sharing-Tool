from django.db import models
from django.conf import settings
import uuid
import json
from datetime import datetime
from django.contrib.auth.models import User as USER_MODEL
from oauth2_provider.settings import oauth2_settings
APPLICATION_MODEL = oauth2_settings.APPLICATION_MODEL


class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    endpoint = models.URLField(blank = True)
    provider = models.BooleanField(default=True)
    owner = models.BooleanField(default=False)
    apple_url = models.URLField(blank = True)
    
    def is_provider(self):
        return provider
    
    def is_owner(self):
        return owner

class EntityOAuth(models.Model):
    entity = models.OneToOneField(Entity, on_delete=models.CASCADE)
    application = models.OneToOneField(APPLICATION_MODEL, on_delete=models.CASCADE)

class OAuthRemoteClient(models.Model):
    token_endpoint = models.URLField()
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    entity = models.OneToOneField(Entity, on_delete=models.CASCADE)
    
class IncidentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length = 255)
    description = models.TextField()
    consequence = models.FloatField()
    provider = models.ForeignKey(Entity, default = getattr(settings, 'SENDER'))
    
    def get_trigger_types(self):
        return TriggerType.objects.filter(incident_type__id = self.id)
    
    def __str__(self):
        return self.name
    
class TriggerType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    incident_type = models.ForeignKey(IncidentType)
    name = models.CharField(max_length = 255)
    description = models.TextField()
    comparators = models.CharField(max_length = 255)
    provider = models.ForeignKey(Entity, default = getattr(settings, 'SENDER'))
    
    def __str__(self):
        return self.name

class NotificationType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length = 255)
    endpoint = models.URLField()
    subscriber = models.ForeignKey(Entity, related_name='subscriptions')
    provider = models.ForeignKey(Entity, default = getattr(settings, 'SENDER'), related_name='provides_subscriptions')
    
    def __str__(self):
        return self.name

class NotificationIncident(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length = 255)
    type = models.ForeignKey(IncidentType)
    notification_type = models.ForeignKey(NotificationType, related_name = 'incidents')
    provider = models.ForeignKey(Entity, default = getattr(settings, 'SENDER'))
    
    def get_triggers(self):
        return NotificationTrigger.objects.filter(notification_incident = self)
    
    def _str__(self):
        return self.name

class NotificationTrigger(models.Model):
    METHODS = (
               ('and', 'AND'),
               ('or', 'OR'),
               ('none', 'NONE'),
               )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.ForeignKey(TriggerType)
    method = models.CharField(max_length = 255, choices = METHODS)
    threshold = models.FloatField()
    comparator = models.CharField(max_length = 1)
    notification_incident = models.ForeignKey(NotificationIncident, related_name = 'triggers')
    provider = models.ForeignKey(Entity, default = getattr(settings, 'SENDER'))


class Liaison(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length = 255)
    email = models.EmailField()
    phone = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255)
    zip = models.CharField(max_length = 19)
    city = models.CharField(max_length = 255)
    provider = models.ForeignKey(Entity, default = getattr(settings, 'SENDER'))
    
    def __str__(self):
        return self.name


TLP_SCHEMA = (
    ('us-cert', 'US-CERT'),
    ('enisa', 'ENISA'),
)

TLP_VALUE = (
    ('red', 'RED'),
    ('amber', 'AMBER'),
    ('green', 'GREEN'),
    ('white', 'WHITE'),
)

class TLP(models.Model):
    schema = models.CharField(max_length=15, choices=TLP_SCHEMA, default='enisa')
    value = models.CharField(max_length=5, choices=TLP_VALUE, default='amber')
    
    @staticmethod
    def from_json(payload):
        if payload:
            data = json.loads(payload)
            
            tlp = TLP()
            tlp.value = data['value']
            tlp.schema = data['schema']
            tlp.save()
            
            for item in data['fields']:
                field = TLPField()
                
                field.field = item['field']
                field.schema = item['schema']
                field.value = item['value']
                
                tlp.add_field(field)
    
    def add_field(self, field):
        field.tlp = self
        field.save()
        self.fields.add(field)
    
    def remove_fields(self):
        TLPField.objects.filter(tlp=self).delete()
    
    def to_json(self):
        return json.dumps(self)

class TLPField(models.Model):
    tlp = models.ForeignKey(TLP, related_name='fields')
    field = models.CharField(max_length=255)
    value = models.CharField(max_length=5, choices=TLP_VALUE, default='amber')
    
    def __str__(self):
        return self.field + ':' + self.value

class Incident(models.Model):
    STATUSES = (
                ('resolved', 'Resolved'),
                ('unresolved', 'Unresolved'),
                )
    
    IMPACT = (
              (1.0, 'High'),
              (0.5, 'Medium'),
              (0.1, 'Low'),
              )
    
    LANGUAGES = (
                 ('en_US', 'English - American'),
                 ('nb_NO', 'Norwegian'),
                 )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    parent = models.UUIDField(null = True, blank = True)
    type = models.ForeignKey(IncidentType)
    language = models.CharField(max_length = 50, choices = LANGUAGES)
    status = models.CharField(max_length = 10, choices = STATUSES)
    impact = models.FloatField(choices = IMPACT)
    summary = models.TextField()
    description = models.TextField()
    occurrence_time = models.DateTimeField()
    detection_time = models.DateTimeField()
    liaison = models.ForeignKey(Liaison)
    provider = models.ForeignKey(Entity, default = getattr(settings, 'SENDER'))
    tlp = models.ForeignKey(TLP, null=True, related_name='incident')
    next_update = models.DateTimeField(null = True, blank = True)
    
    def is_our(self):
        owner = Entity.objects.get(owner = True)
        id = owner.id
        if(self.provider.id == id):
            return True
        
        return False
    
    def is_notified(self):
        status = IncidentNotificationStatus.objects.get(incident = self.id)
        return status.notified
      
    def __str__(self):
        return self.summary

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.ForeignKey(NotificationType, null = True)
    generation_time = models.DateTimeField()
    sent = models.DateTimeField(null = True, blank=True)
    sender = models.CharField(max_length = 255)
    hmac = models.CharField(max_length = 255, blank=True) # TODO: decide how to handle this value
    incidents = models.ManyToManyField(Incident)
    
    @staticmethod
    def create_notification(type, incidents):
        notification = Notification()
        notification.type = type
        notification.generation_time = datetime.now()
        notification.sender = uuid.UUID(getattr(settings, 'SENDER'))
        notification.save()
        
        notification.incidents.add(*incidents)
        
        return notification
    
    def sign_notification(self):
        # TODO Implement HMAC signing of message
        pass

class Attachment(models.Model):
    FORMATS = (
               ('iodef', 'IODEF'),
               ('imdef', 'IMDEF'),
               ('cybox', 'CybOX'),
               ('zip', 'ZIP'),
               ('tar', 'TAR'),
               ('csv', 'CSV'),
               )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    incident = models.ForeignKey(Incident, related_name='attachments', blank=True)
    format = models.CharField(max_length = 255, choices = FORMATS)
    file = models.FileField(null = True, blank = True)
    url = models.URLField()
    
    def _create_file_url(self, file):
        provider = Provider.objects.get(pk = getattr(settings, 'SENDER'))
        file_url = file.url.replace('/api/1.0/files/', '')
        return provider.endpoint + '/files/' + file_url
    
    def save(self, *args, **kwargs):
        if self.file:
            # Add url if file is set
            self.url = self._create_file_url(self.file)
        
        super(Attachment, self).save()

class CustomField(models.Model):
    FIELD_TYPES = (
                   ('string', 'String'),
                   ('int', 'Integer'),
                   ('bool', 'Boolean')
                   )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    incident_type = models.ForeignKey(IncidentType)
    name = models.CharField(max_length = 255)
    description = models.TextField()
    type = models.CharField(max_length = 6, choices = FIELD_TYPES)
    
    def __str__(self):
        return self.name

class CustomFieldValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.ForeignKey(CustomField)
    incident = models.ForeignKey(Incident, related_name='custom_fields')
    value = models.TextField()
    
    def __str__(self):
        return self.value
    
    class Meta:
        unique_together = ('incident', 'type')

class Alert(models.Model):
    ALERT_TYPES = (
                  ('new_incident', 'New Incident'),
                  ('updated_incident', 'Updated Incident'),
                  ('assigned_incident', 'Assigned Incident'),
                  )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length = 255, choices = ALERT_TYPES)
    alert = models.CharField(max_length = 255)
    link = models.URLField()
    notified = models.ManyToManyField(USER_MODEL, through='AlertStatus')

class AlertStatus(models.Model):
    alert = models.ForeignKey(Alert)
    user = models.ForeignKey(USER_MODEL)
    read = models.BooleanField(default = False)

class IncidentNotificationStatus(models.Model):
    incident = models.OneToOneField(Incident, unique = True)
    notified = models.BooleanField(default = False)
