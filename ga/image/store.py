# -*- coding: utf-8 -*-

import StringIO

import shortuuid
from boto.s3.connection import S3Connection

from ga import settings


def upload_image_from_pil_image(image):
    output = StringIO.StringIO()
    image.save(output, 'JPEG')
    output.name = 'file'
    return upload_image(output)


def upload_image(stream):
    conn = S3Connection(settings.AWS_KEY, settings.AWS_SECRET)
    bucket = conn.get_bucket(settings.AWS_BUCKET)

    key = bucket.new_key(shortuuid.uuid() + '.jpg')
    headers = {'Content-Type': 'image/jpeg'}
    key.set_contents_from_string(stream.getvalue(), headers=headers)
    for k, v in headers.items():
        key.set_metadata(k, v)
    key.set_acl('public-read')

    return key.generate_url(expires_in=0, query_auth=False, force_http=True)
