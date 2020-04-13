import datetime

from sqlalchemy import Column, Integer, String, DateTime, orm
from werkzeug.security import generate_password_hash, check_password_hash

from ..db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    email = Column(String, index=True, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    modified_date = Column(DateTime, default=datetime.datetime.now)
    posts = orm.relation('Post', back_populates='author')
    messages = orm.relation('Message', back_populates='author')
    received_messages = orm.relation('Message', back_populates='addressee')

    def __repr__(self):
        return f'<User> {self.id} {self.surname} {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
