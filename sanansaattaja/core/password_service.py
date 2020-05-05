from sanansaattaja.core import ClientError

KEYBOARD = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', 'йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю']


def check_password_security(password: str):
    if len(password) < 8:
        raise ClientError(msg="Password must consist of at least 8 symbols")
    if password == password.lower() or password == password.upper():
        raise ClientError(msg="Password must contain upper and lower case letters")
    num = False
    for i in password:
        if i in '0123456789':
            num = True
            break

    if not num:
        raise ClientError(msg="Password must contain numbers")
    work_pass = password.lower()
    for i in range(1, len(work_pass) - 1):
        for j in KEYBOARD:
            if work_pass[i - 1: i + 2] in j:
                raise ClientError(msg="Password mustn't contain any combination of 3 letters "
                                      "standing next to each other on the keyboard")


def password_check(password, password_again, changing=False):
    if password != password_again:
        if changing:
            raise ClientError(msg="New passwords do not match")
        raise ClientError(msg="Passwords do not match")
    return True
