from sqlalchemy.orm import selectinload

from sanansaattaja.core.errors import ClientError, IdError
from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import Post
from sanansaattaja.db.data.models.comment import Comment
from sanansaattaja.website.forms.comment_form import CommentForm


def get_comments(block_type, block_id):
    session = db_session.create_session()
    comments = session.query(Comment).options(selectinload(Comment.author)).filter(
        (Comment.block_type == block_type) & (Comment.block_id == block_id)).order_by(
        Comment.modified_date.desc()).all()
    session.close()
    return comments


def get_block(block_type, block_id: int):
    session = db_session.create_session()
    if block_type == 'post':
        return session.query(Post).options(selectinload(Post.author)).get(block_id)
    elif block_type == 'comment':
        return get_comment_by_id(block_id)
    session.close()


def add_comment(form: CommentForm, user_id: int, block_type, block_id: int):
    session = db_session.create_session()
    try:
        comment = Comment()
        comment.block_id = block_id
        comment.block_type = block_type
        comment.author_id = user_id
        comment.text = form.text.data
        session.add(comment)
        session.commit()
    except Exception:
        raise ClientError(msg='failed to add a comment')
    session.close()


def delete_comment(comment_id: int):
    session = db_session.create_session()
    comment = session.query(Comment).get(comment_id)
    if not comment:
        raise IdError(msg="There is no such comment")
    if get_comments("comment", comment.id) == []:
        session.delete(comment)
    else:
        comment.is_delete = True
        session.merge(comment)
    session.commit()
    session.close()


def delete_all_comment(block_type, block_id: int):
    comments = get_comments(block_type, block_id)
    if comments != []:
        for i in comments:
            delete_all_comment("comment", i.id)
    if block_type != 'post':
        delete_comment(block_id)
    return


def get_comment_by_id(comment_id):
    session = db_session.create_session()
    comment = session.query(Comment).options(selectinload(Comment.author)).get(comment_id)
    session.close()
    return comment
