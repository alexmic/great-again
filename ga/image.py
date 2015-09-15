# -*- coding: utf-8 -*-
from __future__ import division

import StringIO
from collections import namedtuple
from itertools import izip_longest

from PIL import Image, ImageFont, ImageDraw

from ga import settings


BORDER = Image.open('border.png')


class Banner(object):

    Line = namedtuple('Line', ['x', 'y', 'w', 'h', 'font', 'text'])

    DEFAULT_TEXT_FONT = 'Montserrat-Regular.otf'
    CUSTOM_TEXT_FONT = 'OldStandard-Regular.ttf'

    DEFAULT_TEXT_ABOVE = u'M A K E'
    DEFAULT_TEXT_BELOW = u'G R E A T  A G A I N !'
    DEFAULT_TEXT_FONT_SIZE = 28

    STARTING_Y_OFFSET = 30

    MAX_FONT_SIZE = 75
    MAX_LINE_SPACING = 15

    MIN_FONT_SIZE = 40
    MIN_LINE_SPACING = 78

    def __init__(self, custom_text, image_width=620):
        self.custom_text = custom_text
        self.image_width = image_width

    @property
    def lines(self):
        if hasattr(self, '_lines'):
            return self._lines

        line_config = [
            (self.DEFAULT_TEXT_ABOVE, self.DEFAULT_TEXT_FONT, self.DEFAULT_TEXT_FONT_SIZE)
        ]

        custom_text_font_size = self._get_custom_text_font_size()
        for line in self._split_custom_text_in_lines():
            line_config.append((line, self.CUSTOM_TEXT_FONT, custom_text_font_size))

        line_config.append(
            (self.DEFAULT_TEXT_BELOW, self.DEFAULT_TEXT_FONT, self.DEFAULT_TEXT_FONT_SIZE)
        )

        lines = []
        y_offset = self.STARTING_Y_OFFSET
        for text, font_name, font_size in line_config:
            font = ImageFont.truetype(font_name, font_size)
            tw, th = font.getsize(text)
            x, y = (self.image_width - tw) // 2, y_offset
            lines.append(self.Line(x=x, y=y, w=tw, h=th, font=font, text=text))
            y_offset += th

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
        iterlist = [iter(self.custom_text.split())] * 4
        return [' '.join(filter(None, il)) for il in izip_longest(*iterlist)]


def trumpify_image(image, term):
    image = Image.open(image)
    draw = ImageDraw.Draw(image)

    iw, ih = image.size
    banner = Banner(term.upper(), image_width=iw)

    for line in banner.lines:
        draw.text((line.x, line.y), line.text, font=line.font)

    border_box = (0, 0, settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT)
    image.paste(BORDER, border_box, BORDER)

    out = StringIO.StringIO()
    image.save(out)
    contents = out.getvalue()
    out.close()

    return contents
