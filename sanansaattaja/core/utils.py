import os

from sanansaattaja.core.errors import UserError

KEYBOARD = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', 'йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю']


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


def check_password_security(password: str):
    if len(password) < 8:
        raise UserError(msg="Password must consist of at least 8 symbols")
    if password == password.lower() or password == password.upper():
        raise UserError(msg="Password must contain upper and lower case letters")
    num = False
    for i in password:
        if i in '0123456789':
            num = True
            break

    if not num:
        raise UserError(msg="Password must contain numbers")
    work_pass = password.lower()
    for i in range(1, len(work_pass) - 1):
        for j in KEYBOARD:
            if work_pass[i - 1: i + 2] in j:
                raise UserError(msg="Password mustn't contain any combination of 3 letters "
                                    "standing next to each other on the keyboard")
