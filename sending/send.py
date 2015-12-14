from incidents.models import NotificationIncident, Notification, IncidentNotificationStatus, OAuthRemoteClient
from incidents.serializers import NotificationSerializer
from sending.models import QueueItem

from datetime import datetime
import requests

from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from django.conf import settings

DEBUG = getattr(settings, 'DEBUG')

class Sender(object):
    def __init__(self, request):
        self.request = request
    
    #
    # Notifies subscribers about incidents based on incident type and
    # subscriber defined triggers
    #
    def notify(self, incident):
        incident_type = incident.type
        notification_types = self.get_notification_types(incident_type)
        notifications = self.generate_notifications(notification_types, incident)
        self.process_notifications()
    
    #
    # Fetches all notification types with the affected incident type
    # By assosisation this also fetches the subscribers to be notified
    #
    def get_notification_types(self, incidentType):
        notification_incidents = NotificationIncident.objects.filter(type = incidentType)
        notification_incidents = self.filter_notification_incidents(notification_incidents)
        notification_types = []
         
        for incident in notification_incidents:
            notification_types.append(incident.notification_type)
         
        return notification_types
    
    #
    # Creates notifiations for each subscriber, containing the incident
    #
    def generate_notifications(self, notification_types, incident):
        notifications = []
        
        for type in notification_types:
            incidents = []
            incidents.append(incident)
            notification = Notification.create_notification(type, incidents)
            notification.save()
            notifications.append(notification)
            
            # Add to queue
            item = QueueItem()
            item.notification = notification
            item.send_at = datetime.now()
            item.attempt = 0
            item.save()
        
        return notifications
    
    #
    # Filter notifiations based on triggers, only keeping those which triggers
    # are activated by the incident at hand
    #
    def filter_notification_incidents(self, notification_incidents):
        # Needs to be implemented specifically for each provider or figure out a simple and
        # elegant solution fitting all - probably not easy, if at all possible
        #
        # For now, no filtering is done and no triggers are taken into account
        return notification_incidents
    
    #
    # Queue notifiations for sending
    #
    def process_notifications(self):
        # TODO
        # Needs to be implemented asoncronously - e.g. by using celery
        # Needs to take into account when the notification is to be sent
        #
        queue = QueueItem.objects.order_by('send_at')
        
        for item in queue:
            self.send_notification(item)
    
    #
    # Send a notification from queue
    #
    def send_notification(self, queue_item):
        notification = queue_item.notification
        notification.sent = datetime.now()
        attempt = queue_item.attempt
        queue_item.attempt = attempt + 1
        queue_item.save() 
        
        encoded = NotificationSerializer(notification, context={'request': self.request})
        payload = JSONRenderer().render(encoded.data)

        with open('payload.json', 'w') as jsonfile:
            jsonfile.write(str(payload))
        
        endpoint = notification.type.endpoint
        recipient = notification.type.subscriber
        
        
        params = {'format': 'json'}
        r = requests.post(endpoint, data=payload, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, params=params, verify=False)
        
        
        with open('log.html', 'w') as f:
            f.write(r.text)
        
        
        if r.status_code == requests.codes.created or r.status_code == requests.codes.ok:
            notification.save()
            incidents = notification.incidents.all()
            for incident in incidents:
                IncidentNotificationStatus.objects.update_or_create(incident = incident, defaults={'notified': True})
        
        print("I came here")
        
        queue_item.delete()