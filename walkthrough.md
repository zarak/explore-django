# minimal.py setup

The [four main top level files](https://github.com/syntarsus/minimal-django/blob/master/minimal.py#L1-L6) that are used are `settings`, `url`,
`execute_from_command_line` and `HttpResponse`.
```python
import sys

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.http import HttpResponse
```

Settings file (TODO: see how `.configure` call on settings works)
[User defined settings](https://github.com/syntarsus/minimal-django/blob/65458398b2538a59bb0b4287ff1e10bb8473ea43/minimal.py#L8-L12) are created. Only three values are set. For comparison,
the Django default settings template can be seen [here](https://github.com/django/django/blob/master/django/conf/project_template/project_name/settings.py-tpl).
```python
settings.configure(
    DEBUG=True,
    SECRET_KEY='A-random-secret-key!',
    ROOT_URLCONF=sys.modules[__name__],
)
```

[Function definition](https://github.com/django/django/blob/master/django/conf/__init__.py#L77-L88) for `.configure()`
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

[Function definition](https://github.com/django/django/blob/master/django/core/management/__init__.py#L368-L371) for `execute_from_command_line()`
```python
def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
```

[Function definition](https://github.com/django/django/blob/master/django/core/management/__init__.py#L293-L365) for `execute()`
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

[Function definition](https://github.com/django/django/blob/4a461d49c775331ed52418f007974d61be1e06b9/django/core/management/__init__.py#L188-L217) of `fetch_command`
```python
def fetch_command(self, subcommand):
    """
    Try to fetch the given subcommand, printing a message with the
    appropriate command called from the command line (usually
    "django-admin" or "manage.py") if it can't be found.
    """
    # Get commands outside of try block to prevent swallowing exceptions
    commands = get_commands()
    try:
        app_name = commands[subcommand]
    except KeyError:
        if os.environ.get('DJANGO_SETTINGS_MODULE'):
            # If `subcommand` is missing due to misconfigured settings, the
            # following line will retrigger an ImproperlyConfigured exception
            # (get_commands() swallows the original one) so the user is
            # informed about it.
            settings.INSTALLED_APPS
        else:
            sys.stderr.write("No Django settings specified.\n")
        sys.stderr.write(
            "Unknown command: %r\nType '%s help' for usage.\n"
            % (subcommand, self.prog_name)
        )
        sys.exit(1)
    if isinstance(app_name, BaseCommand):
        # If the command is already loaded, use it directly.
        klass = app_name
    else:
        klass = load_command_class(app_name, subcommand)
    return klass
```

[Function definition](https://github.com/django/django/blob/4a461d49c775331ed52418f007974d61be1e06b9/django/core/management/__init__.py#L40-L72) for `get_commands()`. The docstring for this function is very helpful for understanding what kinds of commands might be available.

```python
@functools.lru_cache(maxsize=None)
def get_commands():
    """
    Return a dictionary mapping command names to their callback applications.

    Look for a management.commands package in django.core, and in each
    installed application -- if a commands package exists, register all
    commands in that package.

    Core commands are always included. If a settings module has been
    specified, also include user-defined commands.

    The dictionary is in the format {command_name: app_name}. Key-value
    pairs from this dictionary can then be used in calls to
    load_command_class(app_name, command_name)

    If a specific version of a command must be loaded (e.g., with the
    startapp command), the instantiated module can be placed in the
    dictionary in place of the application name.

    The dictionary is cached on the first call and reused on subsequent
    calls.
    """
    commands = {name: 'django.core' for name in find_commands(__path__[0])}


    if not settings.configured:
        return commands


    for app_config in reversed(list(apps.get_app_configs())):
        path = os.path.join(app_config.path, 'management')
        commands.update({name: app_config.name for name in find_commands(path)})


    return commands
```

[Function definition](https://github.com/django/django/blob/4a461d49c775331ed52418f007974d61be1e06b9/django/core/management/__init__.py#L30-L37) for `load_command_class()`
```python
def load_command_class(app_name, name):
    """
    Given a command name and an application name, return the Command
    class instance. Allow all errors raised by the import process
    (ImportError, AttributeError) to propagate.
    """
    module = import_module('%s.management.commands.%s' % (app_name, name))
    return module.Command()
```

At this point, presumably `runserver.py` is invoked?
https://github.com/django/django/blob/master/django/core/management/commands/runserver.py

# How does `url` map a regex expression to the `index` model?
Let's look at [`url`](https://github.com/django/django/blob/master/django/conf/urls/__init__.py#L12-L13) next.


```python
def url(regex, view, kwargs=None, name=None):
    return re_path(regex, view, kwargs, name)
```

`re_path` and `_path`
https://github.com/django/django/blob/4a461d49c775331ed52418f007974d61be1e06b9/django/urls/conf.py#L57-L77

```python
def _path(route, view, kwargs=None, name=None, Pattern=None):
    if isinstance(view, (list, tuple)):
        # For include(...) processing.
        pattern = Pattern(route, is_endpoint=False)
        urlconf_module, app_name, namespace = view
        return URLResolver(
            pattern,
            urlconf_module,
            kwargs,
            app_name=app_name,
            namespace=namespace,
        )
    elif callable(view):
        pattern = Pattern(route, name=name, is_endpoint=True)
        return URLPattern(pattern, view, kwargs, name)
    else:
        raise TypeError('view must be a callable or a list/tuple in the case of include().')


path = partial(_path, Pattern=RoutePattern)
re_path = partial(_path, Pattern=RegexPattern)
```
