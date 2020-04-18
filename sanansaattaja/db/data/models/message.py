import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, orm, Text

from ..db_session import SqlAlchemyBase


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    addressee_id = Column(Integer, ForeignKey('users.id'))
    modified_date = Column(DateTime, default=datetime.datetime.now)
    text = Column(Text, nullable=False)
    author = orm.relation('User', foreignKeys=[author_id])
    addressee = orm.relation('User', foreignKeys=[addressee_id])

    def __repr__(self):
        return f'<Message> {self.id} {self.author_id} {self.addressee_id}'
