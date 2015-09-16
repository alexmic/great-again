# -*- coding: utf-8 -*-

import json
import os
from contextlib import contextmanager

from ga import settings


def _resource_directory_path(resource_directory='resources'):
    dirname = os.path.dirname(__file__)
    tokens = dirname.split(os.sep)
    path = ['/']
    for token in tokens:
        if not token:
            continue
        path.append(token)
        if token == settings.PROJECT_ROOT:
            break
    path.append(resource_directory)
    return os.path.join(*path)


RESOURCE_DIRECTORY = _resource_directory_path()


def get_resource_path(filename):
    return os.path.join(RESOURCE_DIRECTORY, filename)


def read_resource_file(filename, from_json=True):
    path = get_resource_path(filename)
    with open(path) as data_file:
        contents = data_file.read()
        return json.loads(contents) if from_json else contents


@contextmanager
def timing(name):
    import time
    start = time.time()
    yield
    print "Timing: name=%s, took=%.2fs" % (name, time.time() - start)
