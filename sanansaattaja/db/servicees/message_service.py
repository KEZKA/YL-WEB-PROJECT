from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import User, Message
from sanansaattaja.db.servicees.user_service import get_user_by_email


def get_all_user_messages(user: User):
    session = db_session.create_session()
    messages = session.query(Message).filter(
        (Message.author_id == user.id) | (Message.addressee_id == user.id)).order_by(
        Message.modified_date.desc()).all()
    return messages


def append_message(form, user: User):
    session = db_session.create_session()
    addressee = get_user_by_email(form.addressee.data)
    message = Message()
    message = message_add_data(message, form, user, addressee)
    session.add(message)
    session.commit()


def message_add_data(message: Message, form, user: User, addressee: User):
    message.text = form.text.data
    message.author_id = user.id
    message.addressee_id = addressee.id
    return message
