from django.views.generic import ListView, CreateView, DetailView
from a_ppl_e.models import EnduserNotification
from a_ppl_e.forms import EnduserNotificationForm

from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from incidents.models import Entity

from braces.views import LoginRequiredMixin
import simplejson as json
import ast
from a_ppl_e.a_ppl_e_library import AppleService


class NotifyEndUserView(LoginRequiredMixin, CreateView):
    form_class = EnduserNotificationForm
    model = EnduserNotification
    template_name = "a_ppl_e/create.html"
    
    def get_initial(self):
        initial = super(NotifyEndUserView, self).get_initial()
        
        resources = self.request.GET.get('resources')
        initial['resources'] = resources
        
        users = self.request.GET.get('users')
        initial['users'] = users
        
        incident = self.kwargs.get('incident')
        initial['incident'] = incident 
        
        return initial
    
    def form_valid(self, form):
        result = super(NotifyEndUserView, self).form_valid(form)
        provider = Entity.objects.get(owner = True)
        url = provider.apple_url
        
        resources_str = self.request.POST.get("resources")
        users_str = self.request.POST.get("users")
        
        resources = []
        users = []
        
        if resources_str is not None:
            resources = ast.literal_eval(resources_str)
        if users_str is not None:
            users = ast.literal_eval(users_str)
        
        appleService = AppleService(url)
        appleService.notify_end_users(users, resources, self.object.message)
        
        return result
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('incident-details', kwargs={'pk': self.kwargs.get('incident')})