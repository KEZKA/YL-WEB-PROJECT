import os

from sanansaattaja.core.errors import PhotoError

MAX_FILE_SIZE = 1024 ** 2


def fullname(name):
    return os.path.join(os.path.dirname(__file__), '..', name)


def load_image(name):
    return fullname('website/static/images/' + name)


def get_photo_from_request(request):
    if request.files['photo']:
        filename = request.files['photo'].filename
        if filename.split('.')[-1].lower() not in ('jpg', 'png', 'gif'):
            raise PhotoError(msg="Invalid extension of image")
        file = request.files['photo'].read(MAX_FILE_SIZE)
        if len(file) == MAX_FILE_SIZE:
            return PhotoError(msg="File size is too large")
    else:
        file = None
    return file
