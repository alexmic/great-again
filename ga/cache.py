# -*- coding: utf-8 -*-

import re
import redis
from ga import settings


redis_client = redis.from_url(settings.REDIS_URL)


class CacheDecorator(object):

    def __init__(self, prefix=None, postfix=None):
        self.prefix = prefix
        self.postfix = postfix

    def __call__(self, fn):
        def wrapper(*args):
            key = _make_key_from_args(*args, prefix=self.prefix, postfix=self.postfix)
            value = redis_client.get(key)
            if not value:
                value = fn(*args)
                redis_client.set(key, value)
            return value

        return wrapper


memoize = CacheDecorator


def incr(*args, **kwargs):
    key = _make_key_from_args(*args, **kwargs)
    redis_client.incr(key)


def _make_key_from_args(*args, **kwargs):
    prefix = kwargs.pop('prefix', None)
    postfix = kwargs.pop('postfix', None)

    prefix = _utf8(prefix + ':' if prefix else '')
    postfix = _utf8(':' + postfix if postfix else '')

    def keyify(arg):
        if isinstance(arg, basestring):
            arg = re.sub(r'\s+', '-', _utf8(arg)).lower()
        return arg

    key = '+'.join([keyify(arg) for arg in args])
    return prefix + key + postfix


def _utf8(arg):
    if isinstance(arg, unicode):
        # Always convert our keys utf8 bytestrings and make sure we don't
        # crash if we cannot.
        arg = arg.encode('utf-8', 'ignore')
    return arg
