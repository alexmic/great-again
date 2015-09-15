# -*- coding: utf-8 -*-

import os
env = os.environ

PROJECT_ROOT = env.get('GA_PROJECT_ROOT', 'ga')

DEBUG = env.get('GA_DEBUG', 'true') == 'true'
TESTING = env.get('GA_TESTING', '') == 'true'

SERVER_NAME = env.get('GA_SERVER_NAME', 'localhost:5000')
SECRET_KEY = '4\xc8Dq\x04R>\x8a\x02\xd5\x95\x0eDx\xd4&\xe5\x83\xf6T\x1e4\xec)'

BOSS_APP_ID = 'IDBmgktA7c'
BOSS_KEY = env.get('GA_BOSS_KEY')
BOSS_SECRET = env.get('GA_BOSS_SECRET')
BOSS_IMAGE_URL = 'https://yboss.yahooapis.com/ysearch/images'
