# -*- coding: utf-8 -*-

from flask import Blueprint, request
from ga.boss import image_url_for_term


blueprint = Blueprint('views', __name__)


@blueprint.route('/random')
def random():
    url = image_url_for_term(request.args.get('term'))
    return 'ok'
