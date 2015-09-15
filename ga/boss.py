# -*- coding: utf-8 -*-

import random
from requests_oauthlib import OAuth1Session
from ga import settings


class BossImage(object):

    def __init__(self, obj):
        self.url = obj['url']
        self.width = int(obj['width'])
        self.height = int(obj['height'])


def image_url_for_term(term, minimum_side=settings.IMAGE_SIDE):
    boss = OAuth1Session(settings.BOSS_KEY, client_secret=settings.BOSS_SECRET)

    params = {'q': term, 'dimensions': 'large'}
    response = boss.get(settings.BOSS_IMAGE_URL, params=params).json()
    results = response['bossresponse']['images']['results']

    def is_valid(i):
        return i.width >= minimum_side and i.height >= minimum_side

    images = [BossImage(r) for r in results]
    choice = random.choice([i for i in images if is_valid(i)])
    return choice.url if choice else None
