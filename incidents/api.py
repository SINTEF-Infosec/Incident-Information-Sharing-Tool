from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.reverse import reverse
from django.contrib.auth.models import User as USER_MODEL

from sending.send import Sender

import ast

from a_ppl_e.a_ppl_e_library import AppleService

from incidents.serializers import *
from incidents.models import *

class Subscriber(generics.CreateAPIView):
    serializer_class = EntitySerializer
    
    def perform_create(self, serializer):
        original = serializer.save()
        original.provider = False
        original.save()
        
        return original

class ProviderIdentity(generics.RetrieveAPIView):
    serializer_class = ProviderSerializer
    
    def get_object(self):
        try:
            return Entity.objects.get(owner = True)
        except IncidentType.DoesNotExist:
            raise Http404

class IncidentTypeList(generics.ListCreateAPIView):
    queryset = IncidentType.objects.all()
    serializer_class = IncidentTypeSerializer

class IncidentTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncidentTypeSerializer
    
    def get_object(self):
        try:
            pk = self.kwargs.get('pk')
            return IncidentType.objects.get(pk=pk)
        except IncidentType.DoesNotExist:
            raise Http404

class TriggerTypeList(generics.ListCreateAPIView):
    serializer_class = TriggerTypeSerializer
    
    def get_queryset(self):
        uuid = self.kwargs.get('incident')
        
        # TODO check if incident type exists
        
        return TriggerType.objects.filter(incident_type__id = uuid)

class TriggerTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TriggerTypeSerializer
    
    def get_object(self):
        try:
            pk = self.kwargs.get('pk')
            return TriggerType.objects.get(pk=pk)
        except TriggerType.DoesNotExist:
            raise Http404

class NotificationTypeList(generics.ListCreateAPIView):
    serializer_class = NotificationTypeSerializer
    
    def get_queryset(self):
        return NotificationType.objects.all()

class NotificationTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationTypeSerializer
    
    def get_object(self):
        try:
            pk = self.kwargs.get('pk')
            return NotificationType.objects.get(pk=pk)
        except Notification.DoesNotExist:
            raise Http404

class NotificationIncidentList(generics.ListCreateAPIView):
    serializer_class = NotificationIncidentSerializer
    
    def get_queryset(self):
        notification = self.kwargs.get('notification')
        return NotificationIncident.objects.filter(notification_type__id = notification)

class NotificationIncidentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationIncidentSerializer
    
    def get_object(self):
        try:
            pk = self.kwargs.get('pk')
            return NotificationIncident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            raise Http404

class NotificationTriggerList(generics.ListCreateAPIView):
    serializer_class = NotificationTriggerSerializer
    
    def get_queryset(self):
        incident = self.kwargs.get('notificationIncident')
        return NotificationTrigger.objects.filter(notification_incident_id = incident)

class NotificationTriggerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationTriggerSerializer
    
    def get_object(self):
        try:
            pk = self.kwargs.get('pk')
            return NotificationTrigger.objects.get(pk=pk)
        except NotificationTrigger.DoesNotExist:
            raise Http404

class ReceiveNotification(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    
    def perform_create(self, serializer):
        original = serializer.save()
        
        incidents = original.incidents
        users = USER_MODEL.objects.all()
        
        incidents = incidents.all()
        for incident in incidents:
            id = incident.id
            url = reverse('incident-details', args=[id], request=self.request)
            type = 'new_incident'
            read = False
            alert = incident.summary
            
            alert, created = Alert.objects.update_or_create(type = type, alert = alert, link = url)
            
            for user in users:
                status, created = AlertStatus.objects.update_or_create(user = user, alert = alert, read = read)
                
                
        return original

class SendNotification(APIView):
    
    def get(self, request, incidentId):
        incident = Incident.objects.get(pk = incidentId)
         
        sender = Sender(request)
        sender.notify(incident)
        
        return Response(status = status.HTTP_200_OK)

class SendEndUserNotification(generics.CreateAPIView):
    serializer_class = EndUserNotificationSerializer
    
    def perform_create(self, serializer):
        original = serializer.save()
        
        url = getattr(settings, 'APPLE_BASE_URL')
        
        users = []
        resources = []
        
        users = ast.literal_eval(original.users)
        resources = ast.literal_eval(original.resources)
        
        print(users)
        print(resources)
        
        appleService = AppleService(url)
        appleService.notify_end_users(users, resources, original.message)        
                
        return original

class IncidentList(generics.ListAPIView):
    serializer_class = IncidentSerializer
    queryset = Incident.objects.all()

class IncidentDetails(generics.RetrieveAPIView):
    serializer_class = IncidentSerializer

class CustomFieldList(generics.ListCreateAPIView):
    serializer_class = CustomFieldSerializer
    page_size = 1000
    
    def get_queryset(self):
        uuid = self.kwargs.get('incidentType')
        
        return CustomField.objects.filter(incident_type__id = uuid)

class CustomFieldValueDetails(APIView):
    serializer_class = CustomFieldValueSerializer
    page_size = 1000
    
    def get(self, request, incident, customFieldType, format= None):
        
        value = CustomFieldValue.objects.get(type__id = customFieldType, incident__id = incident)
        
        serializer = CustomFieldValueSerializer(value)
        
        return Response(serializer.data)
    
    def get_queryset(self):
        uuid = self.kwargs.get('customFieldType')
        incident = self.kwargs.get('incident')
        return CustomFieldValue.objects.get(type__id = uuid, incident__id = incident)

class AlertStatusList(generics.ListCreateAPIView):
    serializer_class = AlertStatusSerializer
    page_size = 1000
    
    def get_queryset(self):
        userId = self.request.user.id
        
        return AlertStatus.objects.filter(user__id = userId, read = False)

class AlertStatusRead(APIView):
    
    def get(self, request, id):
        alert = AlertStatus.objects.get(alert_id = id, user = request.user)
        alert.read = True
        alert.save()
        
        return Response(status = status.HTTP_200_OK)
        