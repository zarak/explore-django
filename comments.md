My digging was into what is the minimal application in Django and how to built on top on it? For this question here are the links like this https://github.com/syntarsus/minimal-django

I'm listing other templates I found at 
https://github.com/mini-kep/full-app/issues/12

I also like the comaprision learning resources (how this is done here and there), new ones I looked at are 
https://www.cis.upenn.edu/~cis192/spring2016/files/lec/lec11.pdf

Specifically - on slide 11 this says: Django will generate an initial setup for you
Makes a directory, 5 files with 138 lines
I wonder what are this files, and how are they different from 
My understanding is that there is a programmatic way of doing things in django with import something + some of those programmatic things are wrapped by configuration files and scripts.

To illustrate:
In here https://github.com/mini-kep/full-app/issues/4#issuecomment-331185026 - settings. configure() does much the same as settings.py
For wrapping in scripts: execute_from_command_line is in managy.py https://github.com/mini-kep/full-app/blob/master/manage.py

In documentation we often get manage.py command
but a closer look should take as to 
Management Utility class https://github.com/django/django/blob/master/django/core/management/__init__.py#L144
There is is easy to see the execution stops the no "apps" are set in settigns.py:
https://github.com/django/django/blob/master/django/core/management/__init__.py#L316-L319

Something not immendiately clear is where is a list of all possible commands to manage.py
In theory - even Django has a very simple cotrol loop in 5-10 statments, which is later hiiden by all kinds of instructions if "you want this - do this", but the core concept kind of disappears
