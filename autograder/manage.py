#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autograder.settings')
    try:
        from django.core.management import execute_from_command_line
        if len(sys.argv) >= 2:
            if sys.argv[1] == 'migrate':
                execute_from_command_line(['manage.py', 'chgroups', 'load'])
            elif sys.argv[1] == "runserver":
                execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if not os.environ.get('RUN_MAIN', False):
        execute_from_command_line(sys.argv)
