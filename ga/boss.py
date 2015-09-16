# -*- coding: utf-8 -*-

from StringIO import StringIO
import random
import re

import grequests
from requests_oauthlib import OAuth1Session
from PIL import Image

from ga import settings
from ga.utils import timing


def escaped_term(term):
    return re.sub(r'\s+', '+', term).lower()


def get_pil_image_for_term(term, minimum_side=settings.IMAGE_SIDE):
    boss = OAuth1Session(settings.BOSS_KEY, client_secret=settings.BOSS_SECRET)

    params = {'q': escaped_term(term), 'dimensions': 'large'}

    with timing('boss.get'):
        response = boss.get(settings.BOSS_IMAGE_URL, params=params).json()

    results = response['bossresponse']['images'].get('results')

    if not results:
        return None

    results = [r for r in results if _is_valid_boss_result(r, minimum_side)]

    if not results:
        return None

    with timing('_pick_readable_images'):
        images = _pick_readable_images(results)

    if not images:
        return None

    return random.choice(images)


def _is_valid_boss_result(result, min_size):
    width = int(result['width'])
    height = int(result['height'])
    format = result['format']
    return width >= min_size and height >= min_size and format in ['jpeg', 'jpg']


def _pick_readable_images(results):
    images, index, batch_size = [], 0, 3
    urls = [r['url'] for r in results]

    while index < len(urls):
        batch = urls[index:index + batch_size]
        index += batch_size

        reqs = (grequests.get(url, timeout=1, allow_redirects=False) for url in batch)

        with timing('grequests.map'):
            responses = grequests.map(reqs)

        for resp in responses:
            if resp is None or resp.status_code != 200:
                continue
            try:
                image = Image.open(StringIO(resp.content))
                images.append(image)
            except IOError:
                continue

        if images:
            break

    return images
