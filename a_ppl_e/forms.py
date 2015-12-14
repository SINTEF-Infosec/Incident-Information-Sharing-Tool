from django import forms
from a_ppl_e.models import EnduserNotification

class EnduserNotificationForm(forms.ModelForm):
    class Meta:
        model = EnduserNotification
        fields = ('incident', 'message', 'users', 'resources')
        
        widgets = {
                   'incident': forms.HiddenInput(),
                   'users': forms.HiddenInput(),
                   'resources': forms.HiddenInput(),
                   }