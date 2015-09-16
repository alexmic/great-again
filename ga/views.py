# -*- coding: utf-8 -*-

import StringIO

from flask import Blueprint, request, render_template, redirect, url_for
import shortuuid

from ga import settings
from ga.boss import image_url_for_term
from ga.image.draw import trumpify_image_from_url
from ga.image.store import upload_image

blueprint = Blueprint('views', __name__)

@blueprint.route('/')
def index():
    return render_template('index.html')


@blueprint.route('/create', methods=['POST'])
def create_image():
    term = request.form['term']
    url = image_url_for_term(term)
    image = trumpify_image_from_url(url, term)

    output = StringIO.StringIO()
    image.save(output, 'JPEG')
    output.name = 'file'

    uploaded = upload_image(output)
    return uploaded


@blueprint.route('/i/<uuid>')
def view_image(uuid):
    return 'ok'
