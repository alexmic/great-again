# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, abort

from ga import cache
from ga.boss import get_pil_image_for_term
from ga.image.draw import trumpify_image_from_url
from ga.image.store import upload_image_from_pil_image
from ga.utils import timing


blueprint = Blueprint('views', __name__)


@cache.memoize(prefix='image')
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


@blueprint.route('/submit', methods=['POST'])
def submit():
    term = request.form['term']
    cache.incr(term, prefix='submissions')
    return redirect('/' + term)


@blueprint.route('/<term>')
def view(term):
    url = get_trumpified_image_url_for_term(term)
    cache.incr(term, prefix='views')
    return render_template('image.html', src=url)
