from django.core.management.base import BaseCommand
from django.apps import apps

# import os


# command informer for manager.py to give info about present models
# in base dir there is iforber bash script for running this command

class Command(BaseCommand):
    help = 'giving some info about current app'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options):
        app_conf = apps.get_app_config(options['app_name'])
        app_models = app_conf.get_models()
        for model in app_models:
            self.write('Model %s has %s instances'
                       % (model._meta.model_name,
                          model.objects.all().__len__()))

    def write(self, value):
        print >> self.stdout, value
        print >> self.stderr, 'error:' + value
