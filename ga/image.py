# -*- coding: utf-8 -*-
from __future__ import division

import cStringIO
import urllib
from collections import namedtuple
from itertools import izip_longest

from PIL import Image, ImageFont, ImageDraw

from ga import settings
from ga.utils import get_resource_path


BORDER = Image.open(get_resource_path('images/border.png'))


class Banner(object):

    Line = namedtuple('Line', ['x', 'y', 'w', 'h', 'font', 'text'])

    DEFAULT_TEXT_FONT = 'Montserrat-Regular.otf'
    DEFAULT_TEXT_ABOVE = u'M A K E'
    DEFAULT_TEXT_BELOW = u'G R E A T  A G A I N !'
    DEFAULT_TEXT_FONT_SIZE = 28
    DEFAULT_TEXT_PADDING = 0

    CUSTOM_TEXT_FONT = 'OldStandard-Regular.ttf'
    CUSTOM_TEXT_PADDING = 10

    STARTING_Y_OFFSET = 60

    MAX_FONT_SIZE = 90
    MIN_FONT_SIZE = 40

    def __init__(self, custom_text, image_width=settings.IMAGE_SIDE):
        self.custom_text = custom_text
        self.image_width = image_width

    @property
    def lines(self):
        if hasattr(self, '_lines'):
            return self._lines

        line_config = [(
            self.DEFAULT_TEXT_ABOVE,
            self.DEFAULT_TEXT_FONT,
            self.DEFAULT_TEXT_FONT_SIZE,
            self.DEFAULT_TEXT_PADDING
        )]

        custom_text_font_size = self._get_custom_text_font_size()
        for line in self._split_custom_text_in_lines():
            line_config.append((
                line,
                self.CUSTOM_TEXT_FONT,
                custom_text_font_size,
                self.CUSTOM_TEXT_PADDING
            ))

        line_config.append((
            self.DEFAULT_TEXT_BELOW,
            self.DEFAULT_TEXT_FONT,
            self.DEFAULT_TEXT_FONT_SIZE,
            self.DEFAULT_TEXT_PADDING
        ))

        lines = []
        y_offset = self.STARTING_Y_OFFSET
        for text, font_name, font_size, padding in line_config:
            font_path = get_resource_path('fonts/' + font_name)
            font = ImageFont.truetype(font_path, font_size)
            tw, th = font.getsize(text)
            x, y = (self.image_width - tw) // 2, y_offset
            lines.append(self.Line(x=x, y=y, w=tw, h=th, font=font, text=text))
            y_offset += th + padding

        self._lines = lines
        return self._lines

    @property
    def bounding_rectangle(self):
        if hasattr(self, '_bounding_rectangle'):
            return self._bounding_rectangle

        min_x, max_x = 10 ** 16, 0
        min_y, max_y = 10 ** 16, 0

        for line in self.lines:
            min_x = min(min_x, line.x)
            max_x = max(max_x, line.x + line.w)
            min_y = min(min_y, line.y)
            max_y = max(max_y, line.y + line.h)

        return min_x, min_y, max_x, max_y

    def _get_custom_text_font_size(self):
        lct = len(self.custom_text)
        if lct <= 7:
            return self.MAX_FONT_SIZE
        size = int(self.MAX_FONT_SIZE - lct * 3.4)
        return max(self.MIN_FONT_SIZE, size)

    def _split_custom_text_in_lines(self):
        lct = len(self.custom_text)
        if lct <= 32:
            return [self.custom_text]
        iterlist = [iter(self.custom_text.split())] * 3
        return [' '.join(filter(None, il)) for il in izip_longest(*iterlist)]


def trumpify_image_from_url(url, term):
    image = get_image_from_url(url)
    image = center_crop(resize(image))
    draw = ImageDraw.Draw(image)

    banner = Banner(term.upper())

    for line in banner.lines:
        draw.text((line.x, line.y), line.text, font=line.font)

    border_box = (0, 0, settings.IMAGE_SIDE, settings.IMAGE_SIDE)
    image.paste(BORDER, border_box, BORDER)

    return image


def get_image_from_url(url):
    contents = cStringIO.StringIO(urllib.urlopen(url).read())
    return Image.open(contents)


def resize(image, side=settings.IMAGE_SIDE):
    iw, ih = image.size
    if iw < ih:
        w, h = side, ih * side / iw
    else:
        w, h = iw * side / ih, side
    return image.resize(map(int, (w, h)))


def center_crop(image, side=settings.IMAGE_SIDE):
    iw, ih = image.size
    left, upper = (iw - side) // 2, (ih - side) // 2
    right, lower = (iw + side) // 2, (ih + side) // 2
    return image.crop((left, upper, right, lower))
