import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, orm, Boolean, Text, String

from sanansaattaja.db.data.db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    modified_date = Column(DateTime, default=datetime.datetime.now)
    text = Column(Text, nullable=False)
    is_public = Column(Boolean, default=False)
    topic = Column(String, nullable=False)
    author = orm.relation('User')

    def __repr__(self):
        return f'<Post> {self.id} {self.author_id}'
