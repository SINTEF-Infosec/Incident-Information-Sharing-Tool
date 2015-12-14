from django.contrib import admin
from incidents.models import *

class TriggerTypeAdmin(admin.StackedInline):
    model = TriggerType
    extra = 0

class CustomFieldsAdmin(admin.StackedInline):
    model = CustomField
    extra = 0

class IncidentTypeAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'consequence']
    list_display = ('name', 'consequence')
    list_filter = ['consequence']
    search_fields = ['name', 'description']
    inlines = [TriggerTypeAdmin, CustomFieldsAdmin]

admin.site.register(IncidentType, IncidentTypeAdmin)


class NotificationTriggerAdmin(admin.StackedInline):
    model = NotificationTrigger
    extra = 0

class NotificationIncidentAdmin(admin.ModelAdmin):
    fields = ['name', 'type', 'notification_type']
    list_display = ['name', 'type', 'notification_type']
    list_filter = ['type', 'notification_type']
    search_fields = ['name']
    inlines = [NotificationTriggerAdmin]

admin.site.register(NotificationIncident, NotificationIncidentAdmin)

class AttachmentAdmin(admin.StackedInline):
    model = Attachment
    extra = 0


class NotificationTypeAdmin(admin.ModelAdmin):
    fields = ['name', 'endpoint', 'subscriber']
    #inlines = [NotificationIncidentAdmin]
    list_display = ('name', 'endpoint', 'subscriber')
    search_fields = ['name']

admin.site.register(NotificationType, NotificationTypeAdmin)

class LiaisonAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'phone', 'address', 'zip', 'city']
    list_display = ('name', 'email', 'phone')
    search_fields = ['name']
    list_filter = ['city']
    
admin.site.register(Liaison, LiaisonAdmin)

class CustomFieldValuesAdmin(admin.StackedInline):
    model = CustomFieldValue
    extra = 0

class IncidentAdmin(admin.ModelAdmin):
    fieldsets = [
                 ('General', {'fields': ['parent', 'type', 'language']}),
                 ('Overview', {'fields': ['status', 'impact', 'summary']}),
                 ('Details', {'fields': ['description', 'occurrence_time', 'detection_time']}),
                 ('Follow up', {'fields': ['liaison']}),
                 ]
    
    inlines = [CustomFieldValuesAdmin, AttachmentAdmin]

admin.site.register(Incident, IncidentAdmin)

class NotificationAdmin(admin.ModelAdmin):
    fields = ['type', 'generation_time', 'sent']
    list_display = ('type', 'generation_time', 'sent')
    list_filter = ['type', 'generation_time', 'sent']
    
    def has_add_permission(self, request):
        return False

admin.site.register(Notification, NotificationAdmin)