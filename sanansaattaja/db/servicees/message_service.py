from sqlalchemy.orm import selectinload

from sanansaattaja.core.errors import MessageError
from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import Message
from sanansaattaja.db.servicees.user_service import get_user_by_email


def get_all_user_messages(user_id: int):
    session = db_session.create_session()
    messages = session.query(Message).options(selectinload('*')).filter(
        (Message.author_id == user_id) | (Message.addressee_id == user_id)).order_by(
        Message.modified_date.desc()).all()
    return messages


def append_message(form, user_id: id):
    session = db_session.create_session()
    addressee = get_user_by_email(form.addressee.data)
    session.merge(addressee)
    message = Message()
    message = message_add_data(message, form, user_id, addressee.id)
    session.add(message)
    session.commit()


def message_add_data(message: Message, form, user_id: int, addressee_id: int):
    message.text = form.text.data
    message.author_id = user_id
    message.addressee_id = addressee_id
    return message

def delete_message(message_id: int):
    session = db_session.create_session()
    message = session.query(Message).get(message_id)
    if not message:
        raise MessageError(msg="There is no such message")
    session.delete(message)
    session.commit()
