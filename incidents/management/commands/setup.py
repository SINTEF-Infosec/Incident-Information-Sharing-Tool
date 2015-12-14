from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from incidents.models import Entity, Liaison

from redbaron import RedBaron
import os
from django.conf import settings
from random import choice
import subprocess

class Command(BaseCommand):
    help = 'Creates initial setup for provider'
    
    def handle(self, *args, **options):
        call_command('migrate', interactive = False)
        
        try:
            company = Entity.objects.get(owner=True)
            self.stdout.write('Already configured')
        except Entity.DoesNotExist:
            entity = Entity()
            entity.name = 'Your company'
            entity.description = 'Your company description'
            entity.endpoint = 'http://localhost:8000/api/1.0'
            entity.provider = True
            entity.owner = True
            entity.save()
            
            
            # Add dummy liaison
            liaison = Liaison()
            liaison.name = 'Your Company Support Center'
            liaison.email = 'support@test.test'
            liaison.phone = '123456789'
            liaison.address = 'Testing Road'
            liaison.zip = '123456'
            liaison.city = 'Testicity'
            liaison.provider = entity
            liaison.save()
            
            base = getattr(settings, 'BASE_DIR')
            settings_path = os.path.join(base, 'Exchange', 'settings.py')
            
            with open(settings_path, 'r+') as f:
                read_data = f.read()
                f.seek(0)
                red = RedBaron(read_data)
                
                red.find("assignment", target=lambda x: x.dumps() == "SENDER").value.replace("'" + str(entity.id) + "'")
                
                secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
                red.find("assignment", target=lambda x: x.dumps() == "SECRET_KEY").value.replace("'" + secret_key + "'")

                f.truncate()
                code = red.dumps()
                
                f.write(code)
            f.closed
            
            print('Database content created')
            print('Provider configured')
            print('New secret key generated')
            
            self.stdout.write('Setup complete')
        