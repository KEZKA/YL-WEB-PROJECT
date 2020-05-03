import os


def fullname(name):
    return os.path.join(os.path.dirname(__file__), '..', name)


def load_image(name):
    return fullname('website/static/images/' + name)
