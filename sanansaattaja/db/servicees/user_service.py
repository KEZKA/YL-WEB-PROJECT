from sanansaattaja.core.errors import ClientError, IdError
from sanansaattaja.core.password_service import password_check, check_password_security
from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import User
from sanansaattaja.website.forms import RegisterForm


def nickname_check(nickname: str):
    try:
        get_user_by_nickname(nickname)
    except ClientError:
        return True
    raise ClientError(msg="This nickname is already in use")


def add_user(form: RegisterForm, file):
    session = db_session.create_session()
    password_check(form.password.data, form.password_again.data)
    nickname_check(form.nickname.data)
    check_password_security(form.password.data)
    user = User()
    user = user_add_data(user, form, file)
    session.add(user)
    session.commit()
    session.close()


def user_add_data(user: User, form, file):
    user.name = form.name.data
    user.surname = form.surname.data
    user.nickname = form.nickname.data
    if form.age.data < 5:
        raise ClientError('You must be older than 5')
    if form.age.data > 122:
        raise ClientError('Oh you are Jeanne Calman? Be serious choose a normal age..')
    user.age = form.age.data
    user.sex = form.sex.data
    if 'password' in dir(form):
        user.set_password(form.password.data)
    user.profile_picture = file
    return user


def edit_user(user_id: int, form, file):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if form.nickname.data != user.nickname:
        nickname_check(form.nickname.data)
    user = user_add_data(user, form, file)
    session.merge(user)
    session.commit()
    session.close()


def edit_password(user_id: int, password_form):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    password_check(password_form.password.data, password_form.password_again.data, changing=True)
    if password_form.password.data == password_form.old_password.data:
        raise ClientError(msg="Old and new passwords mustn't match")
    check_password_security(password_form.password.data)
    user.set_password(password_form.password.data)
    session.merge(user)
    session.commit()
    session.close()


def get_user_by_id(user_id: int):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    session.close()
    if not user:
        raise IdError(msg="There is no such user")
    return user


def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    session.close()
    return users


def get_user_by_nickname(nickname: str):
    session = db_session.create_session()
    user = session.query(User).filter(User.nickname == nickname).first()
    session.close()
    if not user:
        raise ClientError(msg="There is no such user")
    return user


def get_filer_users(args):
    users = get_users()
    if 'nickname' in args:
        users = filter(lambda x: args['nickname'] in x.nickname, users)
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
            raise ClientError(msg="Wrong old password")
        raise ClientError(msg="Wrong password")
    return True
