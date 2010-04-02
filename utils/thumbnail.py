"""
    limited.utils.thumbnail
    ~~~~~~~~~~~~~~~~~~~~~~~
"""
# Thumbnail filter based on code from
# http://batiste.dosimple.ch/blog/2007-05-13-1/

import os
import Image
from django import template
from django.template.defaultfilters import stringfilter
from limited.settings import MEDIA_URL, MEDIA_ROOT, UPLOAD_DIRS
from limited.utils.utils import makepath

register = template.Library()

THUMBNAILS_DIR = 'thumbnails'
# folder to save thumbnails
SCALE_WIDTH = 'w'
SCALE_HEIGHT = 'h'

SCALE_STANDARD_WIDTH = "100"
SCALE_STANDARD_HEIGHT = "100"

def scale(max_x, pair):
    x, y = pair
    new_y = (float(max_x) / x) * y
    return (int(max_x), int(new_y))

@register.filter
def thumbnailize(path, size=SCALE_STANDARD_WIDTH):
    if not path:
        return ""

    original_image_path = os.path.join(MEDIA_ROOT, path)

    if (size.lower().endswith(SCALE_HEIGHT)):
        mode = SCALE_HEIGHT
    else:
        mode = SCALE_WIDTH

    # defining the size
    max_size = int(size.strip())

    # defining the filename and the miniature filename
    basename, format = original_image_path.rsplit('.', 1)
    basename, name = basename.rsplit(os.path.sep, 1)

    miniature = name + '_thumb_' + str(max_size) + mode + '.' + format
    # file name of miniature file
    thumbnail_path = os.path.join(basename, THUMBNAILS_DIR)
    #makepath(thumbnail_path)

    miniature_filename = os.path.join(thumbnail_path, miniature)
    miniature_url = MEDIA_URL + '/'.join(THUMBNAILS_DIR, miniature)

    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename) \
        or os.path.getmtime(original_image_path) > os.path.getmtime(miniature_filename):
        image = Image.open(original_image_path)
        image_x, image_y = image.size

        if mode == SCALE_HEIGHT:
            image_y, image_x = scale(max_size, (image_y, image_x))
        else:
            image_x, image_y = scale(max_size, (image_x, image_y))


        image = image.resize((image_x, image_y), Image.ANTIALIAS)

        image.save(miniature_filename, image.format)

    return miniature_url
