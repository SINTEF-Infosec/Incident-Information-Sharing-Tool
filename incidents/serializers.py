from rest_framework import routers, serializers, viewsets, fields

from incidents.models import *
from a_ppl_e.models import *

class EntitySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    
    class Meta:
        model = Entity
        fields = ('id', 'name', 'description', 'endpoint')
        extra_kwargs = {
                        "id": {
                               "validators": [],
                               },
                        }
        
class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'name', 'description')

class IncidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentType
        fields = ('id', 'name', 'description', 'consequence')
        extra_kwargs = {
                        "id": {
                               "validators": [],
                               },
                        }

class TriggerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriggerType
        fields = ('id', 'name', 'description', 'comparators')

class NotificationTriggerSerializer(serializers.HyperlinkedModelSerializer):
    type = TriggerTypeSerializer(required = False)
    
    class Meta:
        model = NotificationTrigger
        fields = ('id', 'type', 'method', 'threshold', 'comparator')
        extra_kwargs = {
                        "type": {
                               "validators": [],
                               },
                        }

class NotificationIncidentSerializer(serializers.HyperlinkedModelSerializer):
    triggers = NotificationTriggerSerializer(required = False, many = True)
    
    class Meta:
        model = NotificationIncident
        fields = ('id', 'name', 'triggers')

class NotificationTypeSerializer(serializers.ModelSerializer):
    incidents = NotificationIncidentSerializer(required = False, many = True)
    
    class Meta:
        model = NotificationType
        fields = ('id', 'name', 'endpoint', 'incidents')

class LiaisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liaison
        fields = ('id', 'name', 'email', 'phone', 'address', 'zip', 'city')
        extra_kwargs = {
                        "id": {
                               "validators": [],
                               },
                        }

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'format', 'url')
        
        extra_kwargs = {
                        "id": {
                               "validators": [],
                               },
                        }

class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = ('id', 'name', 'description', 'type')
        
        extra_kwargs = {
                        "id": {
                               "validators": [],
                               },
                        }

class CustomFieldValueSerializer(serializers.ModelSerializer):
    type = CustomFieldSerializer(required = True, many = False)
    
    class Meta:
        model = CustomFieldValue
        fields = ('id', 'type', 'value')
        
        extra_kwargs = {
                        "id": {
                               "validators": [],
                               },
                        }

class TLPFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLPField
        fields = ('field', 'value')

class TLPSerializer(serializers.ModelSerializer):
    fields = TLPFieldSerializer(required = False, many = True)
    
    class Meta:
        model = TLP
        field = ('schema', 'value', 'fields')

class IncidentSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(required = False, many = True)
    custom_fields = CustomFieldValueSerializer(required = False, many = True)
    liaison = LiaisonSerializer(required=True, many=False)
    type = IncidentTypeSerializer(required=True, many=False)
    tlp = TLPSerializer(required=False, many=False)
    
    class Meta:
        model = Incident
        fields = ('id', 'parent', 'type', 'language', 'status', 'impact', 'summary', 'description', 'occurrence_time', 'detection_time', 'liaison', 'custom_fields', 'attachments', 'tlp')
        extra_kwargs = {
                        "id": {
                               "validators": [],
                               },
                        }

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ('id', 'type', 'alert', 'link', 'notified')

class AlertStatusSerializer(serializers.ModelSerializer):
    alert = AlertSerializer(required = True, many = False)
    
    class Meta:
        model = AlertStatus
        fields = ('alert', 'read')


class NotificationSerializer(serializers.ModelSerializer):
    incidents = IncidentSerializer(required = False, many = True)
    type = NotificationTypeSerializer(required=True, many=False)
    
    def validate_sender(self, value):
        try:
            Entity.objects.get(id = value)
        except Entity.DoesNotExist:
            raise serializers.ValidationError("The provider is not registered in IMT")
        
        return value
    
    def update(self, validated_data):
        self.create(validated_data)
    
    def create(self, validated_data):
        # Create and store notification
        notification, created = Notification.objects.update_or_create(id = validated_data.get('id'), defaults={'generation_time': validated_data.get('generation_time'), 'sent': validated_data.get('sent'), 'sender': validated_data.get('sender'), 'hmac': validated_data.get('hmac')})
        
        provider = Entity()
        provider.id = notification.sender
        
        # Create and store incidents
        for raw_incident in validated_data.get('incidents'):
            
            incident_type = raw_incident.get('type')
            incident_type, created = IncidentType.objects.update_or_create(id = incident_type.get('id'), defaults={'name': incident_type.get('name'), 'description': incident_type.get('description'), 'consequence': incident_type.get('consequence'), 'provider': provider})
            
            # Create and store TLP information
            tlp = raw_incident.get('tlp')
            
            try:
                tlp_value = TLP.objects.get(incident = raw_incident.get('id'))
            except TLP.DoesNotExist:
                tlp_value = None
            
            if tlp:
                schema = tlp.get('schema')
                value = tlp.get('value')
                if tlp_value:
                    tlp_value, created = TLP.objects.update_or_create(id = tlp_value.id, defaults = {'schema': schema, 'value': value})
                    TLPField.objects.filter(tlp=tlp_value).delete()
                else:
                    tlp_value = TLP.objects.create(schema = schema, value = value)
                
                for item in tlp.get('fields'):
                    field = TLPField()
                    field.field = item.get('field')
                    field.value = item.get('value')
                    field.tlp = tlp_value
                    field.save()
            
            # Create and store liaison
            liaison = raw_incident.get('liaison')
            liaison, created = Liaison.objects.update_or_create(id = liaison.get('id'), defaults={'name': liaison.get('name'), 'email': liaison.get('email'), 'phone': liaison.get('phone'), 'address': liaison.get('address'), 'zip': liaison.get('zip'), 'city': liaison.get('city'), 'provider': provider})
            
            # Create incident
            incident, created = Incident.objects.update_or_create(id = raw_incident.get('id'), defaults={'parent': raw_incident.get('parent'), 'type': incident_type, 'language': raw_incident.get('language'), 'status': raw_incident.get('status'), 'impact': raw_incident.get('impact'), 'summary': raw_incident.get('summary'), 'description': raw_incident.get('description'), 'occurrence_time': raw_incident.get('occurrence_time'), 'detection_time': raw_incident.get('detection_time'), 'liaison': liaison, 'provider': provider, 'tlp': tlp_value})
            notification.incidents.add(incident)

            # Create and store custom field values
            for value in raw_incident.get('custom_fields'):
                raw_type = value.get('type')
                type, created = CustomField.objects.update_or_create(id = raw_type.get('id'), defaults={'name': raw_type.get('name'), 'type': raw_type.get('type'), 'description': raw_type.get('description'), 'incident_type': incident_type})
                
                customField, created = CustomFieldValue.objects.update_or_create(id = value.get('id'), defaults={'type': type, 'value': value.get('value'), 'incident': incident})
            
            # Create and store attachments
            for raw_attachment in raw_incident.get('attachments'):
                attachment, created = Attachment.objects.update_or_create(id = raw_attachment.get('id'), defaults={'format': raw_attachment.get('format'), 'incident': incident, 'url': raw_attachment.get('url')}) 
        
        return notification
    
    class Meta:
        model = Notification
        fields = ('id', 'type', 'generation_time', 'sender', 'hmac', 'incidents')
        read_only_fields = ()

class EndUserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnduserNotification
        fields = ('incident', 'message', 'users', 'resources')
