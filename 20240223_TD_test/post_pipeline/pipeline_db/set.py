# -*- coding: utf-8 -*-

def setup():
    import os
    import django
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post_pipeline.settings')
    django.setup()


setup()

