# -*- coding: utf-8 -*-

import StringIO

import cloudinary
import cloudinary.uploader

from ga import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_KEY,
    api_secret=settings.CLOUDINARY_SECRET
)


def upload_image_from_pil_image(image):
    output = StringIO.StringIO()
    image.save(output, 'JPEG')
    output.name = 'file'
    return upload_image(output)


def upload_image(stream):
    result = cloudinary.uploader.upload(stream)
    return result['url']
