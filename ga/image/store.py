# -*- coding: utf-8 -*-

import cloudinary
import cloudinary.uploader

from ga import settings

cloudinary.config(
    cloud_name = settings.CLOUDINARY_NAME,
    api_key = settings.CLOUDINARY_KEY,  
    api_secret = settings.CLOUDINARY_SECRET  
)

def upload_image(stream):
    result = cloudinary.uploader.upload(stream)
    return result['url']
