import django
import os



def setup():
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'CXS_pipeline.settings'
        django.setup()

setup()