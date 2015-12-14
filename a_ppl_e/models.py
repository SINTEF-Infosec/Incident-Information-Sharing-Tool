from django.db import models

class EnduserNotification(models.Model):
    incident = models.ForeignKey("incidents.Incident")
    message = models.TextField()
    users = models.TextField()
    resources = models.TextField()
    
    @staticmethod
    def get_end_user_notification_for_incident(incidentId):
        return EnduserNotification.objects.filter(incident__id = incidentId).order_by('id')