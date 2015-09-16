# -*- coding: utf-8 -*-

import re
import redis
from ga import settings


redis_client = redis.from_url(settings.REDIS_URL)


class CacheDecorator(object):

    def __init__(self, prefix=None, postfix=None):
        self.prefix = _utf8(prefix + ':' if prefix else '')
        self.postfix = _utf8(':' + postfix if postfix else '')

    def __call__(self, fn):
        def wrapper(*args):
            key = self._make_key(*args)
            value = redis_client.get(key)
            if not value:
                value = fn(*args)
                redis_client.set(key, value)
            return value

        return wrapper

    def _make_key(self, *args):
        key = _make_key_from_args(*args)
        return self.prefix + key + self.postfix


cache = CacheDecorator


def _make_key_from_args(*args):
    def keyify(arg):
        if not isinstance(arg, basestring):
            arg = re.sub(r'\s+', '-', _utf8(arg)).lower()
        return arg
    return '+'.join([keyify(arg) for arg in args])


def _utf8(arg):
    if isinstance(arg, unicode):
        # Always convert our keys utf8 bytestrings and make sure we don't
        # crash if we cannot.
        arg = arg.encode('utf-8', 'ignore')
    return arg
