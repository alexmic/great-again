# -*- coding: utf-8 -*-

from flask import Blueprint, request

from ga import settings
from ga.boss import image_url_for_term
from ga.image import trumpify_image


blueprint = Blueprint('views', __name__)


@blueprint.route('/random')
def random():
    url = image_url_for_term(request.args.get('term'))
    return 'ok'


@blueprint.route('/create', methods=['POST'])
def create_image(self):
    pass