# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect

from ga.cache import cache
from ga.boss import image_url_for_term
from ga.image.draw import trumpify_image_from_url
from ga.image.store import upload_image_from_pil_image


blueprint = Blueprint('views', __name__)


@cache(prefix='term', postfix='image')
def get_trumpified_image_url_for_term(term):
    term = term.lower()
    url = image_url_for_term(term)
    image = trumpify_image_from_url(url, term)
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
