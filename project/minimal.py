import sys
import os

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.http import HttpResponse

BASE_DIR = ''

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='A-random-secret-key!',
        ROOT_URLCONF=sys.modules[__name__],
        DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
        INSTALLED_APPS = ['minimal.apps.MinimalConfig']
    )

def index(request):
    return HttpResponse('<h1>A minimal Django response!</h1>')

urlpatterns = [
    url(r'^$', index),
]


if __name__ == '__main__':
    execute_from_command_line(sys.argv)
    # Display some configured settings
    # print("Installed apps:", settings.INSTALLED_APPS)
    # print("Databases:", settings.DATABASES)
