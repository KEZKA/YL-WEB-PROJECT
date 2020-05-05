import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, orm, Binary
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sanansaattaja.db.data.db_session import SqlAlchemyBase
from .message import Message


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    nickname = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    modified_date = Column(DateTime, default=datetime.datetime.now)
    sex = Column(String, nullable=False)
    profile_picture = Column(Binary, nullable=True)

    posts = orm.relation('Post', back_populates='author')
    messages = orm.relation('Message', back_populates='author', foreign_keys=[Message.author_id])
    received_messages = orm.relation('Message', back_populates='addressee',
                                     foreign_keys=[Message.addressee_id])

    def __repr__(self):
        return f'<User> {self.id} {self.surname} {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
