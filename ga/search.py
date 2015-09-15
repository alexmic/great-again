import requests
import settings
from StringIO import StringIO
from requests_oauthlib import OAuth1Session

class BossImage(object):
    def __init__(self, obj):
        self.url = obj['url']
        self.width = int(obj['width'])
        self.height = int(obj['height'])
    def stream(self):
        r = requests.get(self.url)
        return StringIO(r.content)

def image_for_term(term, minimum_width=1000):
    boss = OAuth1Session(settings.BOSS_KEY,
                         client_secret=settings.BOSS_SECRET)

    try:
        response = boss.get(settings.BOSS_IMAGE_URL, params={'q': term, 'dimensions':'large'}).json()
        results = response['bossresponse']['images']['results']
    except:
        return None

    for result in results:
        img = BossImage(result)
        if img.width >= minimum_width:
            return img.stream()

    return None
