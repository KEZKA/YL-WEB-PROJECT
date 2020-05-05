from sanansaattaja.core.errors import UserError
from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import User

MAX_FILE_SIZE = 1024 ** 2


def password_check(password, password_again, changing=False):
    if password != password_again:
        if changing:
            raise UserError(msg="New passwords do not match")
        raise UserError(msg="Passwords do not match")
    return True


def email_check(email: str):
    try:
        get_user_by_email(email)
    except UserError:
        return True
    raise UserError(msg="This email is already in use")


def add_user(form, file):
    session = db_session.create_session()
    password_check(form.password.data, form.password_again.data)
    email_check(form.email.data)
    check_password_security(form.password.data)
    user = User()
    user = user_add_data(user, form, file)
    session.add(user)
    session.commit()


def user_add_data(user: User, form, file):
    user.name = form.name.data
    user.surname = form.surname.data
    user.email = form.email.data
    user.age = form.age.data
    user.sex = form.sex.data
    if 'password' in dir(form):
        user.set_password(form.password.data)
    user.profile_picture = file
    return user


def user_change_password(user: User, password_form):
    user.set_password(password_form.password.data)
    return user


def edit_user(user_id: int, form, file):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if form.email.data != user.email:
        email_check(form.email.data)
    user = user_add_data(user, form, file)
    session.merge(user)
    session.commit()


def edit_password(user_id: int, password_form):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    password_check(password_form.password.data, password_form.password_again.data, changing=True)
    if password_form.password.data == password_form.old_password.data:
        raise UserError(msg="Old and new passwords mustn't match")
    check_password_security(password_form.password.data)
    user = user_change_password(user, password_form)
    session.merge(user)
    session.commit()


def check_password_security(password: str):
    keyboard = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', 'йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю']

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
        for j in keyboard:
            if work_pass[i - 1: i + 2] in j:
                raise UserError(msg="Password mustn't contain any combination of 3 letters "
                                    "standing next to each other on the keyboard")


def get_user_by_id(user_id: int):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        raise UserError(msg="There is no such user")
    return user


def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return users


def get_user_by_email(email: str):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise UserError(msg="There is no such user")
    return user


def get_filer_users(args):
    users = get_users()
    if 'email' in args:
        users = filter(lambda x: args['email'] in x.email, users)
    if 'name' in args:
        users = filter(lambda x: args['name'] in x.name, users)
    if 'surname' in args:
        users = filter(lambda x: args['surname'] in x.surname, users)
    if 'age' in args:
        users = filter(lambda x: int(args['age']) <= x.age, users)
    if 'sex' in args:
        users = filter(lambda x: args['sex'] in x.sex, users)
    return list(users)


def password_verification(user: User, password: str, changing=False):
    if not user.check_password(password):
        if changing:
            raise UserError(msg="Wrong old password")
        raise UserError(msg="Wrong password")
    return True
