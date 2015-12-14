from django.db import models
from incidents.models import Incident, NotificationType, Notification


class QueueItem(models.Model):
    notification = models.ForeignKey(Notification)
    send_at = models.DateTimeField()
    attempt = models.IntegerField(default=0)