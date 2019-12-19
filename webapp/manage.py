#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import requests


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def startDB():
    url2delete = "http://localhost:7200/rest/repositories/anpc"
    requests.delete(url2delete)
    filepath = os.path.join("app", "rdf", "anpc-config.ttl")
    files = {'config': open(filepath, 'rb')}
    urlrepos = 'http://localhost:7200/rest/repositories'
    requests.post(urlrepos, files=files)
    filepath = os.path.join("app", "rdf", "statements3.rdf")
    header = {"Content-Type": "application/rdf+xml;charset=UTF-8"}
    file = open(filepath, 'rb').read()
    url2insert = 'http://localhost:7200/repositories/anpc/statements'
    requests.post(url2insert, data=file, headers=header)


if __name__ == '__main__':
    startDB()
    main()
