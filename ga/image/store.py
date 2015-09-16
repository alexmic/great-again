# -*- coding: utf-8 -*-

import StringIO

import shortuuid
from boto.s3.connection import S3Connection

from ga import settings


conn = S3Connection(settings.AWS_KEY, settings.AWS_SECRET)
bucket = conn.get_bucket(settings.AWS_BUCKET)

def upload_image_from_pil_image(image):
    output = StringIO.StringIO()
    image.save(output, 'JPEG')
    output.name = 'file'
    return upload_image(output)


def upload_image(stream):
    uuid = shortuuid.uuid()
    key = bucket.new_key(uuid + '.jpg')
    key.set_contents_from_string(stream.getvalue())
    key.set_metadata('Content-Type', 'image/jpeg')
    key.set_acl('public-read')
    return key.generate_url(expires_in=0, query_auth=False, force_http=True)