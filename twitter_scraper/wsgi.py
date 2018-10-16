"""
WSGI config for twitter_scraper project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

path = 'home/ubuntu/twitterDemographics'

if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitter_scraper.settings')

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

#application = get_wsgi_application()
