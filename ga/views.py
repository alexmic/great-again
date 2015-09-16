# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, abort

from ga.cache import cache
from ga.boss import get_pil_image_for_term
from ga.image.draw import trumpify_image_from_url
from ga.image.store import upload_image_from_pil_image
from ga.utils import timing


blueprint = Blueprint('views', __name__)


@cache(prefix='term', postfix='image')
def get_trumpified_image_url_for_term(term):
    term = term.lower()
    with timing('get_pil_image_for_term'):
        image = get_pil_image_for_term(term)
    if not image:
        abort(404)
    with timing('trumpify_image_from_url'):
        image = trumpify_image_from_url(image, term)
    with timing('upload_image_from_pil_image'):
        return upload_image_from_pil_image(image)


@blueprint.route('/')
def index():
    return render_template('index.html')


@blueprint.route('/redirect', methods=['POST'])
def redirect_for_term():
    term = request.form['term']
    return redirect('/' + term)


@blueprint.route('/<term>')
def view_image(term):
    url = get_trumpified_image_url_for_term(term)
    return render_template('image.html', src=url)
