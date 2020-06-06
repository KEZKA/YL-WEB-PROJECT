import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, orm, Text, String, Boolean

from sanansaattaja.core.utils import get_date
from sanansaattaja.db.data.db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    block_id = Column(Integer)
    block_type = Column(String, nullable=False)
    modified_date = Column(DateTime, default=datetime.datetime.now)
    text = Column(Text, nullable=False)
    is_delete = Column(Boolean, default=False)
    author = orm.relation('User')


    def __repr__(self):
        return f'<Comment> {self.id} {self.author_id} {self.post_id}'

    def get_normal_date(self):
        return get_date(self.modified_date)
