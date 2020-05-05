import os

from sanansaattaja.core.errors import ClientError

def fullname(name):
    return os.path.join(os.path.dirname(__file__), '..', name)


def load_image(name):
    return fullname('website/static/images/' + name)


def get_date(datetime):
    months = ['January', 'February', 'March', 'April',
              'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']
    date = months[datetime.month - 1] + ' ' + str(datetime.day) + ', ' + str(datetime.year)
    time = ' at ' + str(datetime.hour) + ':' + str(datetime.minute)
    return date + time