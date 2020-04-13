import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, orm, Boolean, Text

from ..db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    modified_date = Column(DateTime, default=datetime.datetime.now)
    text = Column(Text, nullable=False)
    public = Column(Boolean, default=False)
    author = orm.relation('User')

    def __repr__(self):
        return f'<Post> {self.id} {self.author_id}'
