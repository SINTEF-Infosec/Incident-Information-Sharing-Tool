import requests
from django.conf import settings

DEBUG = getattr(settings, 'DEBUG')

class AppleService(object):
    
    def __init__(self, base_url):
        self.base_url = base_url
    
    def notify_all(self, resources, message):
        for resource in resources:
            data = '{"resource": "' + resource + '", "message": "' + message + '"}'
            self._send("/notification/all", data)
    
    def notify_user(self, user, resources, message):
        for resource in resources:
            data = '{"owner": "' + user + '", "resource": "' + resource + '", "message": "' + message + '"}'
            self._send("/notification", data)
        
    def notify_users(self, users, resources, message):
        for user in users:
            self.notify_user(user, resources, message)
    
    def notify_end_users(self, users, resources, message):
        if users:
            self.notify_users(users, resources, message)
        else:
            self.notify_all(resources, message)
        
    def _send(self, relative_url, data):
        url = self.base_url + relative_url
        r = requests.put(url, data)
        
        if DEBUG:
            f = open('log.html', 'w')
            f.write(r.text)
            f.close()
            
        
    def get_registered_users(self):
        url = self.base_url + "/pii/registeredusers"
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            return
        
        dictionary = r.json()
        return dictionary.get("owners")