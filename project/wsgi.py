# -*- coding: utf-8 -*-
"""WSGI config for project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/

"""

from django.core.wsgi import get_wsgi_application
#from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
#application = Sentry(get_wsgi_application())
application = get_wsgi_application()

# import sys
# s = '\n'.join(sys.path)#b'Hello World!'
# def application(environ, start_response):
#     status = '200 OK'
#     output = str.encode(s)
#     response_headers = [('Content-type', 'text/plain'),
#                         ('Content-Length', str(len(output)))]
#     start_response(status, response_headers)
#     return [output]
