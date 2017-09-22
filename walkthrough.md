# minimal.py setup

The four main top level files that are used are `settings`, `url`,
`execute_from_command_line` and `HttpResponse`.
```python
import sys

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.http import HttpResponse
```

Settings file (TODO: see how `.configure` call on settings works)
User defined settings are created. Only three values are set. For comparison,
the Django default settings template can be seen [here](https://github.com/django/django/blob/master/django/conf/project_template/project_name/settings.py-tpl).
```python
settings.configure(
    DEBUG=True,
    SECRET_KEY='A-random-secret-key!',
    ROOT_URLCONF=sys.modules[__name__],
)
```

Function definition for `.configure()`
```python
def configure(self, default_settings=global_settings, **options):
    """
    Called to manually configure the settings. The 'default_settings'
    parameter sets where to retrieve any unspecified values from (its
    argument must support attribute access (__getattr__)).
    """
    if self._wrapped is not empty:
        raise RuntimeError('Settings already configured.')
    holder = UserSettingsHolder(default_settings)
    for name, value in options.items():
        setattr(holder, name, value)
    self._wrapped = holder
```

This would normally be in `views.py`, input a request and output a response
```python
def index(request):
    return HttpResponse('<h1>A minimal Django response!</h1>')
```

This would normally be in `urls.py`
```python
urlpatterns = [
    url(r'^$', index),
]
```

Main
```python
if __name__ == '__main__':
    execute_from_command_line(sys.argv)
```

# Run the server with the `runserver` command
```python
python minimal.py runserver
```

The `runserver` command is stored in `sys.argv[2]`
```
execute_from_command_line(sys.argv)
```

Function definition for `execute_from_command_line()`
```python
def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
```

Function definition for `execute()`
```python
def execute(self):
    """
    Given the command-line arguments, figure out which subcommand is being
    run, create a parser appropriate to that command, and run it.
    """
```

## Installed apps
```python
settings.INSTALLED_APPS
```
# TBC


Showing the part of `execute` relevant to the `runserver` subcommand
```python
if settings.configured:
    # Start the auto-reloading dev server even if the code is broken.
    # The hardcoded condition is a code smell but we can't rely on a
    # flag on the command class because we haven't located it yet.
    if subcommand == 'runserver' and '--noreload' not in self.argv:
        try:
            autoreload.check_errors(django.setup)()
        except Exception:
            # The exception will be raised later in the child process
            # started by the autoreloader. Pretend it didn't happen by
            # loading an empty list of applications.
            apps.all_models = defaultdict(OrderedDict)
            apps.app_configs = OrderedDict()
            apps.apps_ready = apps.models_ready = apps.ready = True

            # Remove options not compatible with the built-in runserver
            # (e.g. options for the contrib.staticfiles' runserver).
            # Changes here require manually testing as described in
            # #27522.
            _parser = self.fetch_command('runserver').create_parser('django', 'runserver')
            _options, _args = _parser.parse_known_args(self.argv[2:])
            for _arg in _args:
                self.argv.remove(_arg)

```
