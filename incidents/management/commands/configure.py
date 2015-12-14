from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from incidents.models import Entity, Liaison

from redbaron import RedBaron
import os
from django.conf import settings
from random import choice
import subprocess

class Command(BaseCommand):
    help = 'Creates initial configuration for provider'
    
    def handle(self, *args, **options):
        call_command('makemigrations', interactive = False)
        
        print('Database definition updated')
        
        call_command('migrate', interactive = False)
        
        print('Database updated')
        
        self.stdout.write('Configure complete')
        