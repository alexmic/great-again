# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for
import shortuuid

from ga import settings
from ga.boss import image_url_for_term
from ga.image import trumpify_image_from_url


blueprint = Blueprint('views', __name__)


@blueprint.route('/')
def index():
    return render_template('index.html')


@blueprint.route('/create', methods=['POST'])
def create_image():
    term = request.form['term']
    url = image_url_for_term(term)
    image = trumpify_image_from_url(url, term)
    uuid = shortuuid.uuid()
    image.save('/tmp/gen/%s.jpg' % uuid, 'JPEG')
    return redirect('/i/%s' % uuid)


@blueprint.route('/i/<uuid>')
def view_image(uuid):
    src = url_for('static', filename="gen/%s.jpg" % uuid)
    return render_template('image.html', src=src)
