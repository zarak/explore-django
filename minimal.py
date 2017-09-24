"""Minimal code to run Django server.

Adapted from:
   https://github.com/syntarsus/minimal-django

"""

import sys

from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse

#if overrrides <RuntimeError: Settings already configured> error
if not settings.configured:
    settings.configure(
            
        DEBUG=True,
        
        # can also run without sercret key
        #SECRET_KEY='A-random-secret-key!',
        
        # sets urlconf to itself
        ROOT_URLCONF=sys.modules[__name__],
    )


def index(request):
    return HttpResponse('<h1>A minimal Django response!</h1>')


# what does ^$ mean?
urlpatterns = [
    url(r'^$', index),
]

if __name__ == '__main__':
    # more general, accepts many commands 
    
    #from django.core.management import execute_from_command_line
    #execute_from_command_line(sys.argv)
    
    # more specific, one command defined:
    
    # Django will say <Django version 1.11.5, using settings None>
    import django
    django.setup()    
    
    from django.core import management   
    from django.core.management.commands import runserver
    management.call_command(runserver.Command())
